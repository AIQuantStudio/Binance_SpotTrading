from common import singleton

from setting import StrategySetting
from strategy.simple_strategy import SimpleStrategy
from common import Interval, TradeSettingStruct


@singleton
class StrategyFactory:

    def __init__(self):
        self._map_app_id_to_strategy = {}
        
    def create_strategy(self, app_id, setting_data:TradeSettingStruct, symbol, interval:Interval):
        for strategy in StrategySetting.Strategies:
            if strategy["Name"] == setting_data.strategy_name:
                cls = strategy["Class"]
                strategy_obj = eval(cls)(app_id, symbol, interval)
                self._map_app_id_to_strategy[app_id] = strategy_obj
                return strategy_obj
            
    def get_strategy(self, app_id):
        return self._map_app_id_to_strategy.get(app_id)
