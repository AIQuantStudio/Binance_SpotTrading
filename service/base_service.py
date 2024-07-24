from abc import ABC

class BaseService(ABC):

    def __init__(self, name):
        self._name = name
        
    @property
    def name(self):
        return self._name

    def close(self):
        pass
