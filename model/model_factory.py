from model.lstm_v1.lstmv1 import LstmV1


class ModelFactory:
    
    _instance_model = None
    
    @staticmethod
    def load_model(cls):
        ModelFactory._instance_model = eval(cls)()
        return ModelFactory._instance_model
    
    @staticmethod
    def remove_model():
        ModelFactory._instance_model = None
    
    @staticmethod
    def get_model():
        return ModelFactory._instance_model
    
    @staticmethod
    def load_parameters(filename):
        if ModelFactory._instance_model is not None:
            ModelFactory._instance_model.load_parameters(filename)