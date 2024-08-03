from common import singleton
from exchange.binance_account import BinanceAccount
 
 
@singleton
class BinanceFactory:
    
    def __init__(self):
        self._map_model_to_account = {}
    
    def load_account(self, model_id, account_data):
        account = BinanceAccount(account_data)
        
        if not account.connect():
            return False
        
        self._map_model_to_account[model_id] = account
        return True
    
    def remove_account(self, model_id):
        self._map_model_to_account.pop(model_id)

    def get_account(self, model_id):
        return self._map_model_to_account.get(model_id)
    



