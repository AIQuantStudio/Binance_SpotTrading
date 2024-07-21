from model.lstm_v1.lstmv1 import LstmV1


class ModelFactory:
    
    @staticmethod
    def load_model(cls):
        return eval(cls)()