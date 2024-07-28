from abc import ABC, abstractmethod

class BaseModel(ABC):

    def __init__(self, name, id):
        self._name = name
        self._id = id
    
    @property
    def id(self):
        return self._id
    
    @property
    def name(self):
        return self._name
    
    @abstractmethod
    def load_data(self, filename_data):
        pass

    @abstractmethod
    def validate_config(self):
        pass
    
    
