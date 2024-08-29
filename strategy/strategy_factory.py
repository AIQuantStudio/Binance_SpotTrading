from common import singleton

from setting import StrategySetting

@singleton
class StrategyFactory:

    def __init__(self):
        self._map_app_id_to_strategy = {}
        
    def create_strategy(self, app_id, strategy_name):
        for strategy in StrategySetting.Strategies:
            if strategy["Name"] == strategy_name:
                cls = strategy["Class"]
                strategy_obj = eval(cls)(app_id)
                self._map_app_id_to_strategy[app_id] = strategy_obj
                break