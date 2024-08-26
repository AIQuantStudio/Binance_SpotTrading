from common import singleton

from setting import StrategySetting

@singleton
class StrategyFactory:

    def __init__(self):
        self._map_model_id_to_strategy = {}
        
    def create_strategy(self, model_id, strategy_name):
        for strategy in StrategySetting.Strategies:
            if strategy["Name"] == strategy_name:
                cls = strategy["Class"]
                strategy_obj = eval(cls)()
                self._map_model_id_to_strategy[model_id] = strategy_obj
                break