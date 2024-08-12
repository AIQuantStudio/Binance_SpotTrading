from common import singleton
from exchange import BinanceFactory
from exchange import TestFactory
 
 
@singleton
class AccountFactory:
    
    def __init__(self):
        self._map_model_id_to_factory= {}
    
    def load_account(self, model_id, account_data):
        if "DB" in account_data:
            # account = TestFactory()
            self._map_model_id_to_factory[model_id] = TestFactory()
            return TestFactory().load_account(model_id, account_data)
        else:
            # account = BinanceFactory()
            self._map_model_id_to_factory[model_id] = BinanceFactory()
            return BinanceFactory().load_account(model_id, account_data)
        
        # if not account.connect():
        #     return False
        
        
        # return True
    
    def remove_account(self, model_id):
        self._map_model_id_to_factory.get(model_id).remove_account(model_id)
        self._map_model_id_to_factory.pop(model_id)

    def get_account_name(self, model_id):
        # account = self._map_model_id_to_factory.get(model_id).get_account_name(model_id)
        return self._map_model_id_to_factory.get(model_id).get_account_name(model_id)
    
    def get_account(self, model_id):
        return self._map_model_id_to_factory.get(model_id)
    
    def get_asset_balance(self, model_id):
        account = self._map_model_id_to_factory.get(model_id)
        return account.get_all_asset_balance()
    



