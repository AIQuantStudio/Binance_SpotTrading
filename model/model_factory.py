from collections import defaultdict
from model.lstm_v1.lstmv1 import LstmV1


class ModelFactory:
    
    _instance_model = defaultdict(list)
    
    @staticmethod
    def create_model(cls):
        model_list = ModelFactory._instance_model[cls]
        if cls in model_list:
        if cls not in ModelFactory._instance_model:
            
            
            ModelFactory._instance_model = eval(cls)()
            return ModelFactory._instance_model
    
    @staticmethod
    def remove_model():
        ModelFactory._instance_model = None
    
    @staticmethod
    def get_model():
        return ModelFactory._instance_model
    
    @staticmethod
    def load_data(filename):
        if ModelFactory._instance_model is not None:
            ModelFactory._instance_model.load_data(filename)
            
    @staticmethod
    def get_config_dict():
        if ModelFactory._instance_model is not None:
            return ModelFactory._instance_model.get_config()
