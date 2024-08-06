from binance import Client


class BinanceAccount:

    def __init__(self, account_data):
        self.name = account_data.name
        self.id = account_data.id
        self.api_key =  account_data.api_key
        self.api_secret = account_data.secret_key

    def connect(self):
        try:
            self.client = Client(self.api_key, self.api_secret)
            info = self.client.get_account()
        except:
            self.client = None
            return False

        return True

    def get_all_asset_balance(self):
        data = self.client.get_account()
        balances = data["balances"]
        return [balance for balance in balances if float(balance["free"]) > 0 or float(balance["locked"]) > 0]
