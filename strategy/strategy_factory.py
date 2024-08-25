from common import singleton

@singleton
class StrategyFactory:

    def __init__(self):
        self._map_model_id_to_strategy = {}
        
    def create_strategy(self):
        pass