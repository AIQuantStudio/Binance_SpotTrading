from common import singleton

from account.base_account import BaseAccount
from account.test_account import TestAccount
from exchange.binance_account import BinanceAccount


@singleton
class AccountFactory:

    def __init__(self):
        self._map_model_id_to_account = {}

    def load_account(self, model_id, account_data):
        if "DB" in account_data:
            account = TestAccount(model_id, account_data)
            self._map_model_id_to_account[model_id] = account

            # return TestFactory().load_account(model_id, account_data)
        else:
            account = BinanceAccount(model_id, account_data)
            self._map_model_id_to_account[model_id] = account
            # return BinanceFactory().load_account(model_id, account_data)

        return account.connect()

    def remove_account(self, model_id):
        account: BaseAccount = self._map_model_id_to_account.pop(model_id)
        account.close()
        

    def get_name(self, model_id):
        # account = self._map_model_id_to_account.get(model_id).get_account_name(model_id)
        account: BaseAccount = self._map_model_id_to_account.get(model_id)
        return account.name
    
    def get_id(self, model_id):
        # account = self._map_model_id_to_account.get(model_id).get_account_name(model_id)
        account: BaseAccount = self._map_model_id_to_account.get(model_id)
        return account.id

    def is_test(self, model_id):
        account: BaseAccount = self._map_model_id_to_account.get(model_id)
        if isinstance(account, TestAccount):
            return True
        return False

    # def get_account(self, model_id):
    #     return self._map_model_id_to_factory.get(model_id)

    def get_asset_balance(self, model_id):
        account: BaseAccount = self._map_model_id_to_account.get(model_id)
        return account.get_asset_balance()
