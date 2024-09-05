import uuid
import torch
import pandas as pd

from common import singleton
from setting import ModelSetting
from model.base_model import BaseModel
from model.lstm_v1.lstmv1 import LstmV1
from exchange.binance_canvas import BinanceCanvas
from exchange.binance_market import BinanceMarket
from structure import BarStruct


@singleton
class ModelFactory:

    def __init__(self):
        self._instance_models = {}

    @property
    def models(self):
        return ModelSetting.Models
    
    
    def create_model_by_idx(self, idx):
        while True:
            unique_id = str(uuid.uuid4().int)[:8]
            id = int(unique_id)
            if id not in self._instance_models.keys():
                break

        try:
            cls = ModelSetting.Models[idx]["class"]
            model_instance = eval(cls)(id)
        except:
            return -1

        self._instance_models[id] = model_instance
        return id

    def delete_model(self, model_id):
        self._instance_models.pop(model_id)
        
    def get_model(self, model_id):
        return self._instance_models.get(model_id)

    def load_data(self, model_id, filename):
        model: BaseModel = self._instance_models.get(model_id, None)
        if model is None:
            return False
        
        if not model.load_data(filename):
            return False

        return True

    def get_model_name(self, model_id):
        return self._instance_models.get(model_id).name
    
    def get_model_symbol(self, model_id):
        model = self._instance_models.get(model_id)
        return f"{model.base_currency.upper()}{model.quote_currency.upper()}"
    
    def get_model_interval(self, model_id):
        model = self._instance_models.get(model_id)
        return self._instance_models.get(model_id).interval

    def get_model_curreny(self, model_id):
        model = self._instance_models.get(model_id)
        return [model.base_currency, model.quote_currency]
        
    # def create_dataloader(self, model_id, data):
    #     df = pd.DataFrame(data, columns=["datetime", "Open", "High", "Low", "Close", "Volume", "CloseTime", "QuoteVolume", "Trades", "BuyBaseVolume", "BuyQuoteVolume", "Ignored"], dtype=float)
    #     df["datetime"] = pd.to_datetime(df["datetime"] / 1000.0, unit="s")
    #     df.set_index("datetime", inplace=True)

    #     model = self._instance_models.get(model_id)
    #     return model.create_dataloader(df)

    def get_config_dict(self, model_id):
        model = self._instance_models.get(model_id)
        if model is not None:
            return model.get_config()
        
    

    def cuda_is_available(self):
        return torch.cuda.is_available()

    # def predict(self, model_id, gpu=False):
    #     model = self._instance_models.get(model_id)
    #     model.set_device("cuda" if gpu else "cpu")
    #     model.to(model.device)

    #     data = BinanceMarket().get_last_klines(self.get_model_symbol(model_id))
    #     df = pd.DataFrame(data, columns=["datetime", "Open", "High", "Low", "Close", "Volume", "CloseTime", "QuoteVolume", "Trades", "BuyBaseVolume", "BuyQuoteVolume", "Ignored"], dtype=float)
    #     df["datetime"] = pd.to_datetime(df["datetime"] / 1000.0, unit="s")
    #     df.set_index("datetime", inplace=True)
    #     df = df.drop(df.index[-1])

    #     dataloader = model.create_dataloader(df)

    #     return model.predict(dataloader)
    
    def predict(self, model_id, data:list[BarStruct]):
        data_array = []
        for bar in data:
            data_bar = []
            timestamp = bar.datetime.timestamp()
            close = bar.close_price
            volume = bar.volume
            trades = bar.trades
            
            data_bar.append(timestamp)
            data_bar.append(close)
            data_bar.append(volume)
            data_bar.append(trades)
            
            data_array.append(data_bar)
            
        df = pd.DataFrame(data_array, columns=["datetime", "Close", "Volume", "Trades"], dtype=float)
        df["datetime"] = pd.to_datetime(df["datetime"], unit="s")
        df.set_index("datetime", inplace=True)
        
        model = self._instance_models.get(model_id)
        dataloader = model.create_dataloader(df)
        return model.predict(dataloader)[0][0]
