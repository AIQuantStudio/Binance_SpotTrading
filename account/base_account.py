from abc import ABC, abstractmethod

class BaseAccount(ABC):

    def __init__(self, model_id, name, id):
        self._model_id = model_id
        self._name = name
        self._id = id
    
    @property
    def model_id(self):
        return self.model_id
    
    @property
    def id(self):
        return self._id
    
    @property
    def name(self):
        return self._name

    

        
    @abstractmethod
    def connect(self):
        pass
    
    @abstractmethod
    def close(self):
        pass
    
    @abstractmethod
    def get_asset_balance(self):
        pass