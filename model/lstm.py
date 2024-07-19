import torch
import torch.nn as nn
import inspect
from dataclasses import dataclass
# LSTM
# 3 gates
# Forget Gate: ft = sigmoid(Wf * [ht-1, xt] + bf)
# Input Gate:
# it = sigmoid(Wi * [ht-1, xt] + bi)
# Ct(hat) = tanh(WC * [ht-1, xt] + bC)
# Ct = ft * Ct-1 + it * Ct(hat)
# Output Gate:
# ot = sigmoid(Wo * [ht-1, xt] + bo)
# ht = ot * tanh(Ct)
class PricePredictionLSTM(nn.Module):
    def __init__(self, input_size, hidden_size, num_layers, output_size=1):
        super(PricePredictionLSTM, self).__init__()
        self.hidden_size = hidden_size  # Size of the hidden state in the LSTM
        self.num_layers = num_layers    # Number of LSTM layers
        self.lstm = nn.LSTM(input_size, hidden_size, num_layers, batch_first=True)  # LSTM layer
        self.fc = nn.Linear(hidden_size, output_size)  # Fully connected layer for output prediction

    def forward(self, input_data):
        # Initialize hidden and cell states for LSTM
        initial_hidden = torch.zeros(self.num_layers, input_data.size(0), self.hidden_size).to(input_data.device)
        initial_cell = torch.zeros(self.num_layers, input_data.size(0), self.hidden_size).to(input_data.device)
        
        # Forward propagate through LSTM
        lstm_output, _ = self.lstm(input_data, (initial_hidden, initial_cell))  # Output shape: (batch_size, seq_length, hidden_size)
        
        # Pass the output of the last time step through the fully connected layer
        last_time_step_output = lstm_output[:, -1, :]  # Extract the output from the last time step
        output = self.fc(last_time_step_output)  # Output shape: (batch_size, output_size)
        return output
    
class ImprovedPricePredictionLSTM(nn.Module):
    def __init__(self, input_size, hidden_size, num_layers, output_size=1, dropout=0.2):
        super(ImprovedPricePredictionLSTM, self).__init__()
        self.hidden_size = hidden_size
        self.num_layers = num_layers
        self.lstm = nn.LSTM(input_size, hidden_size, num_layers, batch_first=True, bidirectional=True)
        self.fc = nn.Linear(hidden_size * 2, output_size)  # Multiply by 2 for bidirectional
        self.fc.SCALE_INIT = 1
        self.dropout = nn.Dropout(dropout)

    def forward(self, x):
        # Initialize hidden states
        h0 = torch.zeros(self.num_layers * 2, x.size(0), self.hidden_size).to(x.device)  # Multiply by 2 for bidirectional
        c0 = torch.zeros(self.num_layers * 2, x.size(0), self.hidden_size).to(x.device)  # Multiply by 2 for bidirectional
        
        # Forward propagate LSTM
        out, _ = self.lstm(x, (h0, c0))  # out: tensor of shape (batch_size, seq_length, hidden_size * 2)
        # Apply dropout to the output of the last time step
        out = self.dropout(out[:, -1, :])  # Output shape: (batch_size, hidden_size * 2)
        # Pass the output through the fully connected layer
        out = self.fc(out)  # Output shape: (batch_size, output_size)
        return out
    
@dataclass
class ModelConfig:
    # Set up hyperparameters
    hidden_units: int = 64 # the amount of internal memory cells of our model, imagine they are small little algorithsm, helping the model to learn
    num_layers: int = 4 # the amount of layers in the model, where each layer contains its own memory cells
    learning_rate: float = 0.001 # the amount the model adapts it's weights and biases (parameters) after every step
    learning_rate_step_size:int = 5 # after how many steps should the learning rate be de- or increased?
    learning_rate_gamma: float = 0.9 # that's the multiplier to manipulate the learning rate
    num_epochs: int = 300 # how many times (steps) our main loop will go through the training process?
    batch_size: int = 32 # how many data will we process at once?
    window_size: int = 14  # how many data points in the past to look at for our prediction
    prediction_steps: int = 7 # how many data points to skip until the data point that we want to predict
    dropout_rate: float = 0.2 # how many nodes in the model to set to zero
    init_norm_std: float = 0.02
    init_norm_mean: float = 0
    sample_size = 1000
    features = ['close', 'volume', 'trades'] # what columns to use 
    target = 'close' # what column to predict
    
class TradeModel(nn.Module):

    def __init__(self, config, process_rank = 0, num_processes = 1):
        super().__init__()
        self.config = config
        self.master_process = process_rank == 0 or num_processes == 1
        # self.process_rank = process_rank
        # self.master_process = process_rank == 0

        self.model = ImprovedPricePredictionLSTM(input_size=len(self.config.features), # 3, ['close', 'volume', 'trades']
                                                 hidden_size=self.config.hidden_units, # 64 by default
                                                 num_layers=self.config.num_layers,    # 4 by default
                                                 dropout = self.config.dropout_rate)    # 0.2 by default
        
        self.loss_fn = nn.MSELoss()
        # init params
        self.apply(self._init_weights)

    def _init_weights(self, module):
        # print(module.__class__.__name__,)
        if isinstance(module, nn.Linear):
            std = self.config.init_norm_std
            if hasattr(module, 'SCALE_INIT'):
                std *= (self.config.num_layers) ** -0.5
            print(module.__class__.__name__, std)
            torch.nn.init.normal_(module.weight, mean=self.config.init_norm_mean, std=std)
            if module.bias is not None:
                torch.nn.init.zeros_(module.bias)
        # elif isinstance(module, nn.Embedding):
        #     torch.nn.init.normal_(module.weight, mean=self.config.init_norm_mean, std=self.config.init_norm_std)

    def configure_optimizers(self, weight_decay, learning_rate, device_type):
        # start with all of the candidate parameters (that require grad)
        param_dict = {pn: p for pn, p in self.named_parameters()}
        param_dict = {pn: p for pn, p in param_dict.items() if p.requires_grad}
        # create optim groups. Any parameters that is 2D will be weight decayed, otherwise no.
        # i.e. all weight tensors in matmuls + embeddings decay, all biases and layernorms don't.
        decay_params = [p for n, p in param_dict.items() if p.dim() >= 2]
        nodecay_params = [p for n, p in param_dict.items() if p.dim() < 2]
        optim_groups = [
            {'params': decay_params, 'weight_decay': weight_decay},
            {'params': nodecay_params, 'weight_decay': 0.0}
        ]
        num_decay_params = sum(p.numel() for p in decay_params)
        num_nodecay_params = sum(p.numel() for p in nodecay_params)
        if self.master_process:
            print(f"num decayed parameter tensors: {len(decay_params)}, with {num_decay_params:,} parameters")
            print(f"num non-decayed parameter tensors: {len(nodecay_params)}, with {num_nodecay_params:,} parameters")
        # Create AdamW optimizer and use the fused version if it is available
        fused_available = 'fused' in inspect.signature(torch.optim.AdamW).parameters
        use_fused = fused_available and device_type == "cuda"
        if self.master_process:
            print(f"using fused AdamW: {use_fused}")
        optimizer = torch.optim.AdamW(optim_groups, lr=learning_rate, betas=(0.9, 0.95), eps=1e-8, fused=use_fused)
        return optimizer

    def forward(self, inputs, targets=None):
        outputs = self.model(inputs) # calculate predictions
        loss = None
        if targets is not None:
            loss = self.loss_fn(outputs.squeeze(), targets) # calculat the loss
        return outputs, loss


if __name__ == '__main__':
    model = TradeModel(ModelConfig())
    

        