from dataclasses import dataclass


@dataclass
class ModelConfig:
    # Set up hyperparameters
    use_compile: bool = False
    hidden_units: int = 128 # the amount of internal memory cells of our model, imagine they are small little algorithsm, helping the model to learn
    num_layers: int = 8 # the amount of layers in the model, where each layer contains its own memory cells
    weight_decay: float = 0.1
    learning_rate: float = 6e-4 # the amount the model adapts it's weights and biases (parameters) after every step
    learning_rate_step_size:int = 5 # after how many steps should the learning rate be de- or increased?
    learning_rate_gamma: float = 0.9 # that's the multiplier to manipulate the learning rate
    num_epochs: int = 300 # how many times (steps) our main loop will go through the training process?
    batch_size: int = 32 # how many data will we process at once?
    window_size: int = 32  # how many data points in the past to look at for our prediction
    prediction_steps: int = 4 # how many data points to skip until the data point that we want to predict
    dropout_rate: float = 0.2 # how many nodes in the model to set to zero
    init_norm_std: float = 0.02
    init_norm_mean: float = 0
    sample_size = 0
    features = ['close', 'volume', 'trades'] # what columns to use 
    target = 'close' # what column to predict
    