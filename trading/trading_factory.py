from common import singleton

from trading.trading_daemon import TradingDaemon
 
 
@singleton
class TradingFactory:
    
    def __init__(self):
        self._map_model_id_to_trading_daemon = {}
    
    def create_daemon(self, model_id):
        daemon = TradingDaemon(model_id)
        self._map_model_id_to_trading_daemon[model_id] = daemon
        return daemon
    
    def get_daemon(self, model_id):
        return self._map_model_id_to_trading_daemon.get(model_id)
        
    
        
    
    


