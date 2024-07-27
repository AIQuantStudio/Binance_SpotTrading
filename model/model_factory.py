import uuid
from collections import defaultdict
from model.lstm_v1.lstmv1 import LstmV1


class ModelFactory:
    
    _instance_models = {}
    
    @staticmethod
    def create_model(name):
        unique_id = str(uuid.uuid4().int)[:8]
        id = int(unique_id)
        # id = uuid.ShortUUID().random(length=22)
        instance = eval(name)(id)
        ModelFactory._instance_models[id] = instance
        return id
    
    @staticmethod
    def remove_model(model_id):
        ModelFactory._instance_models.pop(model_id)

    @staticmethod
    def get_model(model_id):
        return ModelFactory._instance_models.get(model_id)
    
    @staticmethod
    def load_data(model_id, filename):
        model = ModelFactory._instance_models.get(model_id)
        if model is not None:
            model.load_data(filename)
            
    @staticmethod
    def get_config_dict(model_id):
        model = ModelFactory._instance_models.get(model_id)
        if model is not None:
            return model.get_config()
