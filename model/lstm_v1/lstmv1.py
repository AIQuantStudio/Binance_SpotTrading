import torch
import numpy as np


class LstmV1:

    def __init__(self, pair, scaler, config, device):  # data loader
        self.device = device
        self.pair = pair
        self.scaler = scaler
        self.config = config
        self.dataloader = dataloader
        self.dataloader_train = dataloader.dataloader_train
        self.dataloader_val = dataloader.dataloader_val
        self.dataloader_test = dataloader.dataloader_test

        torch.set_float32_matmul_precision("high")
        self.model = TradeModel(config=config)
        self.model.to(self.device)

        self.raw_model = self.model.module if self.ddp else self.model  # always contains the "raw" unwrapped model


        self.all_model_stats = {}
        self.current_model_stats = {
            "name": self.raw_model.model.__class__.__name__,
            "device": self.device,
            "optimizer": self.optimizer.__class__.__name__,
            "sample_size": self.config.sample_size,
            "hidden_units": self.config.hidden_units,
            "num_layers": self.config.num_layers,
            "learning_rate": self.config.learning_rate,
            "batch_size": self.config.batch_size,
            "window_size": self.config.window_size,
            "prediction_steps": self.config.prediction_steps,
            "dropout_rate": self.config.dropout_rate,
            "duration": 0,
            "epochs": [],
            "train_loss_values": [],
            "test_loss_values": [],
            "train_rmse_values": [],
            "test_rmse_values": [],
        }

        current_model_id = (
            self.current_model_stats["name"],
            self.current_model_stats["device"],
            self.current_model_stats["optimizer"],
            self.current_model_stats["sample_size"],
            self.current_model_stats["hidden_units"],
            self.current_model_stats["num_layers"],
            self.current_model_stats["learning_rate"],
            self.current_model_stats["batch_size"],
            self.current_model_stats["window_size"],
            self.current_model_stats["prediction_steps"],
            self.current_model_stats["dropout_rate"],
        )

        self.current_model_id = "|".join(map(str, current_model_id))
        
    def load(self):
        pass

    def predict(self):
        self.model.eval()
        # scaler = StandardScaler()
        # Iterate over the test DataLoader to generate predictions
        predicted_close = np.zeros((0, 1))

        print(f"dataloader_test: {len(self.dataloader_test)}")
        for batch_idx, (inputs, targets) in enumerate(self.dataloader_test):
            inputs = inputs.to(self.device)
            targets = targets.to(self.device)
            # print(f'inputs: {inputs.shape}, targets: {targets.shape}')
            with torch.inference_mode():
                output, _ = self.model(inputs=inputs, targets=targets)
                # predicted_array = np.array(output).reshape(-1, 1)
                # targets_array = np.array(targets).reshape(-1, 1)
                predicted_array = output.detach().cpu().numpy().reshape(-1, 1)
                targets_array = targets.cpu().numpy().reshape(-1, 1)

                dummy_columns = np.zeros((predicted_array.shape[0], 2))  # Assuming 2 dummy columns
                predicted_array_with_dummy = np.concatenate((predicted_array, dummy_columns), axis=1)
                predicted_close_with_dummy = self.scaler.inverse_transform(predicted_array_with_dummy)
                predicted_close_batch = predicted_close_with_dummy[:, :-2]  # Remove the last two columns
                # print(f'predicted_close = {predicted_close.shape}, predicted_close_batch = {predicted_close_batch.shape}')
                predicted_close = np.vstack([predicted_close, predicted_close_batch])
                # actual_array_with_dummy = np.concatenate((targets_array, dummy_columns), axis=1)
                # actual_close_with_dummy = self.scaler.inverse_transform(actual_array_with_dummy)
                # actual_close = actual_close_with_dummy[:, :-2]  # Remove the last two columns
                # print(predicted_close)
                # print(f'output = {output.shape}, targets = {targets.shape}, predicted_array = {predicted_array.shape}, predicted_close = {predicted_close.shape}, actual_close = {actual_close.shape}')
                # for idx in range(inputs.shape[0]):
                #     print(f'Batch = {batch_idx}, Index = {idx},  predicted: {predicted_close[idx]}, actual = {actual_close[idx]}')
            # break
        # print(f'predicted_close = {predicted_close.shape}, predicted_close_batch = {predicted_close_batch.shape}')
        return predicted_close
