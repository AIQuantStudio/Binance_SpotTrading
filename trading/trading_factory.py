from common import singleton

# from common import TradeMode
from trading.trading_daemon import TradingDaemon
from model import ModelFactory
from strategy import StrategyFactory
 
 
@singleton
class TradingFactory:
    
    def __init__(self):
        self._map_app_id_to_trading_daemon = {}
    
    def create_daemon(self, app_id, trade_mode, setting_data):
        # 模型参数
        model_config = ModelFactory().get_config_dict(app_id)
        symbol = ModelFactory().get_model_symbol(app_id)
        interval = ModelFactory().get_model_interval(app_id)
        strategy = StrategyFactory().create_strategy(app_id, setting_data, symbol, interval)
        
        daemon = TradingDaemon(app_id, trade_mode, strategy, setting_data)
        self._map_app_id_to_trading_daemon[app_id] = daemon
        return daemon
    
    def remove_daemon(self, app_id):
        daemon:TradingDaemon = self._map_app_id_to_trading_daemon[app_id]
        daemon.close()
        
    def get_daemon(self, app_id):
        return self._map_app_id_to_trading_daemon.get(app_id, None)
        
    
        
    
    


