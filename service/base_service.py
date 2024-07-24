from abc import ABC

class BaseService(ABC):

    name = ""

    def __init__(self):
        pass

    def close(self):
        pass
