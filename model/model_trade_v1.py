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
    
 
    
class ModelTradeV1:
    def __init__(self, pair, scaler, config, dataloader):  # data loader
        self.pair = pair
        self.scaler = scaler
        self.config = config
        self.dataloader = dataloader
        self.dataloader_train = dataloader.dataloader_train
        self.dataloader_val = dataloader.dataloader_val
        self.dataloader_test = dataloader.dataloader_test
        (
            self.ddp,
            self.ddp_rank,
            self.ddp_local_rank,
            self.ddp_world_size,
            self.master_process,
            self.device,
        ) = self.getDDP()
        # if self.master_process:
        print(
            f"ddp_rank = {self.ddp_rank}, ddp_local_rank = {self.ddp_local_rank}, ddp_world_size = {self.ddp_world_size}, master_process = {self.master_process}, device = {self.device}"
        )
        torch.set_float32_matmul_precision("high")
        self.model = TradeModel(config=config, process_rank=self.ddp_rank, num_processes=self.ddp_world_size)
        self.model.to(self.device)

        if self.config.use_compile:
            self.model = torch.compile(self.model)
        if self.ddp:
            self.model = DDP(self.model, device_ids=[self.ddp_local_rank])
        self.raw_model = (
            self.model.module if self.ddp else self.model
        )  # always contains the "raw" unwrapped model

        self.optimizer = self.raw_model.configure_optimizers(
            weight_decay=self.config.weight_decay,
            learning_rate=self.config.learning_rate,
            device_type=self.device,
        )
        self.scheduler = lr_scheduler.StepLR(
            self.optimizer,
            step_size=self.config.learning_rate_step_size,
            gamma=self.config.learning_rate_gamma,
        )  # Adjust step_size and gamma as needed

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

    def getDDP(self):
        # vanilla, non-DDP run
        ddp_rank = 0
        ddp_local_rank = 0
        ddp_world_size = 1
        master_process = True
        # attempt to autodetect device
        device = "cpu"
        if torch.cuda.is_available():
            device = "cuda"
        elif hasattr(torch.backends, "mps") and torch.backends.mps.is_available():
            device = "mps"
        print(f"using device: {device}")
        ddp = int(os.environ.get("RANK", -1)) != -1  # is this a ddp run?
        if ddp:
            # use of DDP atm demands CUDA, we set the device appropriately according to rank
            assert torch.cuda.is_available(), "for now i think we need CUDA for DDP"
            init_process_group(backend="nccl")
            ddp_rank = int(os.environ["RANK"])
            ddp_local_rank = int(os.environ["LOCAL_RANK"])
            ddp_world_size = int(os.environ["WORLD_SIZE"])
            device = f"cuda:{ddp_local_rank}"
            torch.cuda.set_device(device)
            master_process = (
                ddp_rank == 0
            )  # this process will do logging, checkpointing etc.

        return ddp, ddp_rank, ddp_local_rank, ddp_world_size, master_process, device

    def train(self):
        # Main loop
        start = time.time()

        epoch_count = self.current_model_stats["epochs"]
        start_epoch = (
            0 if len(epoch_count) == 0 else epoch_count[-1]
        )  # helpful if you start over this particular cell

        for epoch in tqdm(
            range(start_epoch, start_epoch + self.config.num_epochs)
        ):  # tqdm is our progress bar wrapper
            self.raw_model.train()  # activate training mode

            # handle loss monitoring
            total_train_loss = 0.0
            all_train_targets = []
            all_train_outputs = []

            # process batches in the training dataloader
            for batch_idx, (inputs, targets) in enumerate(self.dataloader_train):
                # print(f'batch_idx= {batch_idx}, inputs size = {inputs.shape}')
                inputs = inputs.to(self.device)
                targets = targets.to(self.device)
                # with torch.autocast(device_type=device_type, dtype=torch.bfloat16):
                outputs, loss = self.raw_model(
                    inputs=inputs, targets=targets
                )  # calculate predictions

                # if master_process:
                #     print(f'outputs.shape = {outputs.shape}, loss = {loss}')
                self.optimizer.zero_grad()  # reset gradients
                loss.backward()  # backward propagation
                self.optimizer.step()  # update parameters

                total_train_loss += loss.item()
                # print(f'targets = {targets.shape}')
                all_train_targets.extend(targets.cpu().numpy())
                all_train_outputs.extend(outputs.detach().cpu().numpy())
                # print(targets.numpy())
                # print(outputs.detach().numpy())
                # break
            # break
            self.scheduler.step()

            if (
                epoch % int(self.config.num_epochs / 10) == 0
                or epoch == self.config.num_epochs - 1
            ):
                self.raw_model.eval()  # activate eval mode

                # handle loss monitoring
                total_test_loss = 0.0
                all_test_targets = []
                all_test_outputs = []

                # process batches in the testing dataloader
                for i, (inputs, targets) in enumerate(self.dataloader_val):
                    with torch.inference_mode():  # activate inference mode/no grad
                        inputs = inputs.to(self.device)
                        targets = targets.to(self.device)
                        outputs, loss = self.raw_model(
                            inputs=inputs, targets=targets
                        )  # calculate predictions

                        # monitor loss
                        total_test_loss += loss.item()
                        all_test_targets.extend(targets.cpu().numpy())
                        all_test_outputs.extend(outputs.detach().cpu().numpy())

                average_epoch_test_loss = total_test_loss / len(self.dataloader_val)
                test_rmse = math.sqrt(
                    mean_squared_error(all_test_targets, all_test_outputs)
                )

            # calculate average epoch losses
            average_epoch_train_loss = total_train_loss / len(self.dataloader_train)

            # caculate accuracy
            train_rmse = math.sqrt(
                mean_squared_error(all_train_targets, all_train_outputs)
            )

            # VISUALIZE
            self.current_model_stats["epochs"].append(epoch)
            self.current_model_stats["train_loss_values"].append(
                average_epoch_train_loss
            )
            self.current_model_stats["test_loss_values"].append(average_epoch_test_loss)
            self.current_model_stats["train_rmse_values"].append(train_rmse)
            self.current_model_stats["test_rmse_values"].append(test_rmse)

            if (
                epoch % int(self.config.num_epochs / 10) == 0
                or epoch == self.config.num_epochs - 1
            ):
                current_lr = self.scheduler.get_last_lr()[0]
                print(
                    f"Epoch [{epoch + 1}/{start_epoch + self.config.num_epochs}], "
                    f"Train Loss: {average_epoch_train_loss:.4f} | "
                    f"Test Loss: {average_epoch_test_loss:.4f} | "
                    f"Train RMSE: {train_rmse:.4f} | "
                    f"Test RMSE: {test_rmse:.4f} | "
                    f"Current LR: {current_lr:.8f} | "
                    f"Duration: {time.time() - start:.0f} seconds"
                )

        self.current_model_stats["duration"] += time.time() - start
        self.all_model_stats[self.current_model_id] = self.current_model_stats

    def save_model(self, directory="models"):
        model_path = Path(directory)
        model_path.mkdir(parents=True, exist_ok=True)

        model_name = f"model_{self.pair}.pth"
        model_save_path = model_path / model_name

        torch.save(obj=self.model.state_dict(), f=model_save_path)

    def load_model(self, directory="models"):
        model_path = Path(directory)
        model_path.mkdir(parents=True, exist_ok=True)

        model_name = f"model_{self.pair}.pth"
        model_save_path = model_path / model_name
        self.model = TradeModel(
            config=self.config,
            process_rank=self.ddp_rank,
            num_processes=self.ddp_world_size,
        )
        self.model.load_state_dict(torch.load(model_save_path))
        self.model.to(self.device)

        if self.config.use_compile:
            self.model = torch.compile(self.model)
        if self.ddp:
            self.model = DDP(self.model, device_ids=[self.ddp_local_rank])
        self.raw_model = (
            self.model.module if self.ddp else self.model
        )  # always contains the "raw" unwrapped model

        # self.model = TradeModel(config=self.config, process_rank=self.ddp_rank, num_processes=self.ddp_world_size)
        # self.raw_model.load_state_dict(torch.load(model_save_path))
        # self.raw_model.to(self.device)
        # model_loaded.state_dict()

    def _create_sequences(self, data):
        X = []
        y = []
        for i in range(
            len(data) - self.config.window_size - self.config.prediction_steps + 1
        ):
            sequence = data.iloc[i : i + self.config.window_size][self.config.features]
            target = data.iloc[
                i + self.config.window_size + self.config.prediction_steps - 1
            ][self.config.targets]
            X.append(sequence)
            y.append(target)
            # print(X)
            # print(y)

        return np.array(X), np.array(y)

    def predict(self, df, validation_size=10000):
        # df_validation = df[features].head(window_size + prediction_steps).copy() just test one window
        df_validation = df[self.config.features].head(validation_size).copy()

        # actuall we don't need to re-initialize the scaler again
        # scaler = MinMaxScaler()
        scaler = StandardScaler()

        # Extract the selected features and transform them
        selected_features = df_validation[self.config.features].values.reshape(
            -1, len(self.config.features)
        )
        scaled_features = scaler.fit_transform(selected_features)

        # Replace the original features with the scaled features in the DataFrame
        df_validation[self.config.features] = scaled_features

        # MERGING
        X_validate, y_validate = self._create_sequences(df_validation)

        # BATCHING
        # Convert NumPy arrays to PyTorch tensors
        X_validate_tensor = torch.Tensor(X_validate)
        y_validate_tensor = torch.Tensor(y_validate)

        self.model.eval()
        # Iterate over the test DataLoader to generate predictions
        with torch.inference_mode():
            output = self.model(X_validate_tensor)

        predicted_array = np.array(output).reshape(-1, 1)
        dummy_columns = np.zeros(
            (predicted_array.shape[0], 2)
        )  # Assuming 2 dummy columns
        predicted_array_with_dummy = np.concatenate(
            (predicted_array, dummy_columns), axis=1
        )
        predicted_close_with_dummy = scaler.inverse_transform(
            predicted_array_with_dummy
        )
        predicted_close = predicted_close_with_dummy[
            :, :-2
        ]  # Remove the last two columns
        return predicted_close

    def predict_test(self):
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

                dummy_columns = np.zeros(
                    (predicted_array.shape[0], 2)
                )  # Assuming 2 dummy columns
                predicted_array_with_dummy = np.concatenate(
                    (predicted_array, dummy_columns), axis=1
                )
                predicted_close_with_dummy = self.scaler.inverse_transform(
                    predicted_array_with_dummy
                )
                predicted_close_batch = predicted_close_with_dummy[
                    :, :-2
                ]  # Remove the last two columns
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

    def plot_prediction(self, predicted_close):
        plt.figure(figsize=(12, 5))

        # print(f'predicted_close: {predicted_close.shape}, actual close = {self.dataloader.df_sampled_test["close"].shape}')
        y_axis_max = (
            max(np.amax(predicted_close), max(self.dataloader.df_sampled_test["close"]))
            * 1.25
        )
        y_axis_min = (
            min(np.amin(predicted_close), min(self.dataloader.df_sampled_test["close"]))
            * 0.75
        )
        print(f"y_axis_max = {y_axis_max}, y_axis_min = {y_axis_min}")

        print("***************************")
        print(predicted_close[:100])
        print(self.dataloader.df_sampled_test["close"][:100])
        # y_axis_max = max(self.dataloader.df_sampled_test['close']) * 1.25
        # y_axis_min = min(self.dataloader.df_sampled_test['close']) * 0.75
        plt.plot(
            self.dataloader.df_sampled_test.index,
            self.dataloader.df_sampled_test["close"],
            label="Actual",
            color="blue",
        )
        plt.ylabel("Close Price")
        plt.legend()
        plt.legend(loc="upper left")
        plt.ylim(y_axis_min, y_axis_max)

        ax2 = plt.twinx()  # Create a second y-axis sharing the same x-axis

        nan_values = np.full(
            self.config.window_size + self.config.prediction_steps - 1, np.nan
        )
        predicted_close_with_nan = np.concatenate([nan_values, predicted_close.ravel()])

        plt.plot(
            self.dataloader.df_sampled_test.index,
            predicted_close_with_nan,
            label="Predicted",
            color="red",
        )
        plt.ylim(y_axis_min, y_axis_max)

        plt.xlabel("Time")
        plt.title("Actual vs. Predicted Data", fontsize=10)

        # Set different y-axis for actual and predicted data
        ax2.set_ylabel("Predicted Data")

        # Adjust x-axis ticks and labels for better readability
        # plt.xticks(fontsize=8)  # Set font size for x-axis ticks
        # plt.gca().xaxis.set_major_locator(ticker.MaxNLocator(nbins=3))  # Set the number of ticks (change nbins as needed)
        # plt.legend()
        # plt.legend(loc='upper right')

        plt.show()

    def plot(self):
        epoch_count = self.current_model_stats["epochs"]
        plt.figure(figsize=(12, 5))

        # PLOT LOSS
        plt.subplot(1, 3, 1)
        plt.plot(
            epoch_count,
            self.current_model_stats["train_loss_values"],
            label="Train Loss",
        )
        plt.plot(
            epoch_count, self.current_model_stats["test_loss_values"], label="Test Loss"
        )
        plt.xlabel("Epochs")
        plt.ylabel("Loss")
        plt.title(
            f'Training and Test Loss after {self.current_model_stats["duration"]:.0f} seconds',
            fontsize=10,
        )
        plt.legend()

        # PLOT RMSE
        plt.subplot(1, 3, 2)
        plt.plot(
            epoch_count,
            self.current_model_stats["train_rmse_values"],
            label="Train RMSE",
            color="blue",
        )
        plt.plot(
            epoch_count,
            self.current_model_stats["test_rmse_values"],
            label="Test RMSE",
            color="red",
        )

        plt.ylabel("Accuracy (RMSE)")
        plt.xlabel("Epochs")
        plt.title(
            f'Training and Test Accuracy (RMSE) after {self.current_model_stats["duration"]:.0f} seconds',
            fontsize=10,
        )
        plt.legend(loc="upper right")

        # # PLOT PREDICTIONS
        # df_visualize = df.head(validation_size).copy()
        # y_axis_max = max(np.amax(predicted_close), max(df_visualize['close'])) * 1.25
        # y_axis_min = min(np.amin(predicted_close), min(df_visualize['close'])) * 0.75

        # plt.subplot(1, 3, 3)

        # plt.plot(df_visualize.index, df_visualize['close'], label='Actual', color='blue')
        # plt.ylabel('Close Price')
        # plt.legend()
        # plt.legend(loc='upper left')
        # plt.ylim(y_axis_min, y_axis_max)

        # plt.twinx()  # Create a second y-axis sharing the same x-axis

        # nan_values = np.full(window_size + prediction_steps - 1, np.nan)
        # predicted_close_with_nan = np.concatenate([nan_values, predicted_close.ravel()])

        # plt.plot(df_visualize.index, predicted_close_with_nan, label='Predicted', color='red')
        # plt.ylim(y_axis_min, y_axis_max)

        # plt.xlabel('Time')
        # plt.title('Actual vs. Predicted Data', fontsize=10)

        # # Set different y-axis for actual and predicted data
        # ax2.set_ylabel('Predicted Data')

        # # Adjust x-axis ticks and labels for better readability
        # plt.xticks(fontsize=8)  # Set font size for x-axis ticks
        # plt.gca().xaxis.set_major_locator(ticker.MaxNLocator(nbins=3))  # Set the number of ticks (change nbins as needed)
        # plt.legend()
        # plt.legend(loc='upper right')

        # plt.tight_layout()
        plt.show()
