from common import singleton

from trading.trade_daemon import TradeDaemon
 
 
@singleton
class TradingFactory:
    
    def __init__(self):
        self._map_model_id_to_trading_daemon = {}
    
    def create_daemon(self, model_id):
        daemon = TradeDaemon(model_id)
        self._map_model_id_to_trading_daemon[model_id] = daemon
        
    
        
    
    


