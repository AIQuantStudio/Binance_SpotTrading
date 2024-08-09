from abc import ABC, abstractmethod

class BaseModel(ABC):

    def __init__(self, name, id):
        self._name = name
        self._id = id
        self._base_currency = ""
        self._quote_currency = ""
        self._dataloader = None
        self._device = "cpu"
    
    @property
    def id(self):
        return self._id
    
    @property
    def name(self):
        return self._name
    
    @property
    def device(self):
        return self._device
    
    @property
    def dataloader(self):
        return self._dataloader
    
    @property
    def base_currency(self):
        return self._base_currency
    
    @property
    def quote_currency(self):
        return self._quote_currency
    
    def set_device(self, device):
        self._device = device
        
    @abstractmethod
    def load_data(self, filename):
        pass
    
    @abstractmethod
    def create_dataloader(self, data):
        pass
    
    @abstractmethod
    def predict(self, dataloader):
        pass
    
    @abstractmethod
    def to(self, device):
        pass