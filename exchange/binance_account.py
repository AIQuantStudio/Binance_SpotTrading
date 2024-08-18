from binance import Client
from account.base_account import BaseAccount

class BinanceAccount(BaseAccount):

    def __init__(self, model_id, account_data):
        super().__init__(model_id, account_data["Name"], account_data["Account"])
        # self.name = account_data["Name"]
        # self.id = account_data["Account"]
        self.api_key =  account_data["ApiKey"]
        self.api_secret = account_data["SecertKey"]

    def connect(self):
        try:
            self.client = Client(self.api_key, self.api_secret)
            info = self.client.get_account()
        except:
            self.client = None
            return False

        return True
    
    def close(self):
        self.client.close_connection()

    def get_asset_balance(self):
        data = self.client.get_account()
        balances = data["balances"]
        return [balance for balance in balances if float(balance["free"]) > 0 or float(balance["locked"]) > 0]
