import uuid
import pandas as pd
from model.lstm_v1.lstmv1 import LstmV1


def singleton(cls):
    instances = {}
    def wrapper(*args, **kwargs):
        if cls not in instances:
            instances[cls] = cls(*args, **kwargs)
        return instances[cls]
    return wrapper

    
@singleton
class ModelFactory:
    def __init__(self):
        self._instance_models = {}
    
    def create_model(self, name):
        unique_id = str(uuid.uuid4().int)[:8]
        id = int(unique_id)
        try:
            model_instance = eval(name)(id)
        except:
            return -1
        
        self._instance_models[id] = model_instance
        return id
    
    def load_data(self, model_id, filename):
        model = self._instance_models.get(model_id)
        if model is not None:
            model.load_data(filename)
            print(model.validate_config())
            if not model.validate_config():
                return False
            
            return True
    
    def remove_model(self, model_id):
        self._instance_models.pop(model_id)

    def get_model(self, model_id):
        return self._instance_models.get(model_id)
  
    def create_dataloader(self, model_id, data):
        df = pd.DataFrame(data, columns=["datetime", "Open", "High", "Low", "Close", "Volume", "CloseTime", "QuoteVolume", "Trades", "BuyBaseVolume", "BuyQuoteVolume", "Ignored"], dtype=float)
        df["datetime"] = pd.to_datetime(df["datetime"] / 1000.0, unit="s")
        df.set_index("datetime", inplace=True)
        
        model = self._instance_models.get(model_id)
        return model.create_dataloader(df)
            
    def get_config_dict(self, model_id):
        model = self._instance_models.get(model_id)
        if model is not None:
            return model.get_config()
        
 