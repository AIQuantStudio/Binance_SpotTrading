import torch
import numpy as np
from dataclasses import asdict
from sklearn.preprocessing import MinMaxScaler, StandardScaler
from torch.utils.data import TensorDataset, DataLoader

from model.base_model import BaseModel
from model.lstm_v1.model_config import ModelConfig
from model.lstm_v1.lstmv1_module import LstmV1Model




class LstmV1(BaseModel):

    features = ['Close', 'Volume', 'Trades']

    def __init__(self, id):
        super().__init__("LstmV1", id)
        self.scaler = None 
        self.config = None
        self.symbol = None
            
        # self.device = device
        # self.pair = pair
        # self.scaler = scaler
        # self.config = config
        # self.dataloader = dataloader
        # self.dataloader_train = dataloader.dataloader_train
        # self.dataloader_val = dataloader.dataloader_val
        # self.dataloader_test = dataloader.dataloader_test

        # torch.set_float32_matmul_precision("high")
        # self.model = LstmV1Model(config=self.config)
        # self.model.to(self.device)

        # self.raw_model = self.model.module if self.ddp else self.model  # always contains the "raw" unwrapped model


        # self.all_model_stats = {}
        # self.current_model_stats = {
        #     "name": self.raw_model.model.__class__.__name__,
        #     "device": self.device,
        #     "optimizer": self.optimizer.__class__.__name__,
        #     "sample_size": self.config.sample_size,
        #     "hidden_units": self.config.hidden_units,
        #     "num_layers": self.config.num_layers,
        #     "learning_rate": self.config.learning_rate,
        #     "batch_size": self.config.batch_size,
        #     "window_size": self.config.window_size,
        #     "prediction_steps": self.config.prediction_steps,
        #     "dropout_rate": self.config.dropout_rate,
        #     "duration": 0,
        #     "epochs": [],
        #     "train_loss_values": [],
        #     "test_loss_values": [],
        #     "train_rmse_values": [],
        #     "test_rmse_values": [],
        # }

        # current_model_id = (
        #     self.current_model_stats["name"],
        #     self.current_model_stats["device"],
        #     self.current_model_stats["optimizer"],
        #     self.current_model_stats["sample_size"],
        #     self.current_model_stats["hidden_units"],
        #     self.current_model_stats["num_layers"],
        #     self.current_model_stats["learning_rate"],
        #     self.current_model_stats["batch_size"],
        #     self.current_model_stats["window_size"],
        #     self.current_model_stats["prediction_steps"],
        #     self.current_model_stats["dropout_rate"],
        # )

        # self.current_model_id = "|".join(map(str, current_model_id))
        
    def load_data(self, filename_data):
        try:
            checkpoint = torch.load(filename_data, map_location='cpu')
            # self.symbol = checkpoint["symbol"]
            self.symbol = "ADA_USDT"
            self._base_currency = self.symbol.split("_")[0]
            self._quote_currency = self.symbol.split("_")[1]
            self.config = ModelConfig(**checkpoint["model_config"])
            self.scaler = checkpoint["model_scaler"]
            print(self.scaler)
            print(self.scaler.n_samples_seen_)
            print(self.scaler.mean_)
            print(self.scaler.var_)
            print(self.scaler.scale_)
            
            self.model = LstmV1Model(config=self.config)
            self.model.load_state_dict(checkpoint["model_state_dict"])
            # self.model.to("cuda")
        except:
            return False
        
        return True

    def get_config(self):
        return asdict(self.config)


    def predict(self, dataloader):
        self.model.eval()
        # scaler = StandardScaler()
        # Iterate over the test DataLoader to generate predictions
        # predicted_close = np.zeros((0, 1))

        print(f"dataloader_test: {len(dataloader)}")
        for batch_idx, (inputs, targets) in enumerate(dataloader):
            inputs = inputs.to(self.device)
            targets = targets.to(self.device)
            # print(f'inputs: {inputs.shape}, targets: {targets.shape}')
            with torch.inference_mode():
                output, _ = self.model(inputs=inputs, targets=targets)
                print("Number of dimensions:", output.ndim)
                print("Shape of Tensor:", output.shape)
                print("Elements number along axis 0 of Tensor:", output.shape[0])
                print("Elements number along the last axis of Tensor:", output.shape[-1])
                print('Number of elements in Tensor: ', output.numel())
                print("Data Type of every element:", output.dtype)
                print(output[0,0].item())

                # o:torch.Tensor = output[0][0]
                # print(o.values)
                o = np.array([[output[0,0].item(), 0.0, 0.0]])
                d = self.scaler.inverse_transform(o)
    
                
                
                # # predicted_array = np.array(output).reshape(-1, 1)
                # # targets_array = np.array(targets).reshape(-1, 1)
                # predicted_array = output.detach().cpu().numpy().reshape(-1, 1)
                # targets_array = targets.cpu().numpy().reshape(-1, 1)

                # dummy_columns = np.zeros((predicted_array.shape[0], 2))  # Assuming 2 dummy columns
                # predicted_array_with_dummy = np.concatenate((predicted_array, dummy_columns), axis=1)
                # predicted_close_with_dummy = self.scaler.inverse_transform(predicted_array_with_dummy)
                # predicted_close_batch = predicted_close_with_dummy[:, :-2]  # Remove the last two columns
                # # print(f'predicted_close = {predicted_close.shape}, predicted_close_batch = {predicted_close_batch.shape}')
                # predicted_close = np.vstack([predicted_close, predicted_close_batch])
                # # actual_array_with_dummy = np.concatenate((targets_array, dummy_columns), axis=1)
                # # actual_close_with_dummy = self.scaler.inverse_transform(actual_array_with_dummy)
                # # actual_close = actual_close_with_dummy[:, :-2]  # Remove the last two columns
                # # print(predicted_close)
                # # print(f'output = {output.shape}, targets = {targets.shape}, predicted_array = {predicted_array.shape}, predicted_close = {predicted_close.shape}, actual_close = {actual_close.shape}')
                # # for idx in range(inputs.shape[0]):
                # #     print(f'Batch = {batch_idx}, Index = {idx},  predicted: {predicted_close[idx]}, actual = {actual_close[idx]}')
            
            
            
            # break
        # print(f'predicted_close = {predicted_close.shape}, predicted_close_batch = {predicted_close_batch.shape}')
        return d

    def create_dataloader(self, df):
        self.df_sampled = df[self.features].copy()
        self.df_sampled_original = self.df_sampled.copy()
        #scaler = MinMaxScaler() # MinMax would work, too, but in fact a stock price has not really "min/max values", except the 0 ;)
        # self.scaler = StandardScaler()

        # Extract the selected features and transform them
        selected_features = self.df_sampled[self.features].values.reshape(-1, len(self.features))
        # print(selected_features)
        # print(f'selected_features = {selected_features.shape}')
        scaled_features = self.scaler.transform(selected_features)
        # print(f'df_sampled = {type(self.df_sampled[self.features])}, scaled_features = {type(scaled_features)}')
        # Replace the original features with the scaled features in the DataFrame
        self.df_sampled[self.features] = scaled_features

        # MERGING
        print(self.config)
        X, y = self.create_sequences(self.df_sampled, self.config.window_size, self.config.prediction_steps)
        print(X.shape)
        X = X[-1:]
        print(X.shape)
        print(y.shape)
        X_tensor = torch.Tensor(X)
        y_tensor = torch.Tensor([0])
        dataset = TensorDataset(X_tensor, y_tensor)
        dataloader = DataLoader(dataset, batch_size=1, shuffle=False)
        return dataloader
        
        
        
        
        # print(f'X = {len(X)}')
        # SPLITTING
        # X_train, X_temp, y_train, y_temp = train_test_split(X, y, test_size=(1.0 - self.ratio_train), shuffle=False)
        # # print(f'X_train = {len(X_train)}, X_temp = {len(X_temp)}')
        # ratio_val_test = (1.0 - self.ratio_val) / (1.0 - self.ratio_train)
        # X_val, X_test, y_val, y_test = train_test_split(X_temp, y_temp,  test_size=ratio_val_test, shuffle=False)

        # self.df_sampled_train = self.df_sampled_original[:len(X_train)]
        # self.df_sampled_val = self.df_sampled_original[len(X_train):(len(X_train) + len(X_val))]
        # self.df_sampled_test = self.df_sampled_original[(len(X_train) + len(X_val)):]

        # print(f'X_train = {len(X_train)}-{len(self.df_sampled_train)}, X_val = {len(X_val)}-{len(self.df_sampled_val)}, X_test = {len(X_test)}-{len(self.df_sampled_test)}')
        # # BATCHING
        # X_train_tensor = torch.Tensor(X_train)
        # # print(f'X_train_tensor = {X_train_tensor.shape}')
        # y_train_tensor = torch.Tensor(y_train)
        # X_val_tensor = torch.Tensor(X_val)
        # y_val_tensor = torch.Tensor(y_val)
        # X_test_tensor = torch.Tensor(X_test)
        # print(X_test_tensor.shape)
        # y_test_tensor = torch.Tensor(y_test)
        # print(y_test_tensor.shape)

        # train_dataset = TensorDataset(X_train_tensor, y_train_tensor)
        # val_dataset = TensorDataset(X_val_tensor, y_val_tensor)
        # test_dataset = TensorDataset(X_test_tensor, y_test_tensor)

        # # Shuffling is set to "True", if you want to reproduce results, it may help to set shuffle to False
        # self.dataloader_train = DataLoader(train_dataset, batch_size=self.batch_size, shuffle=True) 
        # self.dataloader_val = DataLoader(val_dataset, batch_size=self.batch_size, shuffle=False)
        # self.dataloader_test = DataLoader(test_dataset, batch_size=self.batch_size, shuffle=False)
        # if self.master_process:
        #     print(f'dataloader_train = {len(self.dataloader_train)}, dataloader_val = {len(self.dataloader_val)}, dataloader_test = {len(self.dataloader_test)}')
            
        # return DataLoader()
            
    def create_sequences(self, df, window_size, prediction_steps):
        X = []
        y = []
        for i in range(len(df) - window_size - prediction_steps + 1):
            sequence = df.iloc[i:i + window_size][self.features]
            # target = df.iloc[i + window_size + prediction_steps - 1][self.targets]
            X.append(sequence)
            # y.append(target)
            # print(X)
            # print(y)
        
        return np.array(X), np.array(y)
    
    def to(self, device):
        self.model.to(device)