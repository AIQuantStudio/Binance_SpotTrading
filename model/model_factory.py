import shortuuid
from collections import defaultdict
from model.lstm_v1.lstmv1 import LstmV1


class ModelFactory:
    
    _instance_models = {}
    
    @staticmethod
    def create_model(name):
        id = shortuuid.ShortUUID().random(length=22)
        instance = eval(name)(id)
        ModelFactory._instance_models[id] = instance
        return instance
    
    @staticmethod
    def remove_model():
        ModelFactory._instance_model = None
    
    @staticmethod
    def get_model(name, id):
        return ModelFactory._instance_model
    
    @staticmethod
    def load_data(filename):
        if ModelFactory._instance_model is not None:
            ModelFactory._instance_model.load_data(filename)
            
    @staticmethod
    def get_config_dict():
        if ModelFactory._instance_model is not None:
            return ModelFactory._instance_model.get_config()
