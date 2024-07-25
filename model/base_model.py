from abc import ABC

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

    def close(self):
        pass
