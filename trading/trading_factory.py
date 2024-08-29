from common import singleton

# from structure import TradeMode
from trading.trading_daemon import TradingDaemon
 
 
@singleton
class TradingFactory:
    
    def __init__(self):
        self._map_model_id_to_trading_daemon = {}
    
    def create_daemon(self, model_id,  trade_mode, strategy, setting_data):
        daemon = TradingDaemon(model_id, trade_mode, strategy, setting_data)
        self._map_model_id_to_trading_daemon[model_id] = daemon
        return daemon
    
    def remove_daemon(self, model_id):
        daemon:TradingDaemon = self._map_model_id_to_trading_daemon[model_id]
        daemon.close()
        
    def get_daemon(self, model_id):
        return self._map_model_id_to_trading_daemon.get(model_id, None)
        
    
        
    
    


