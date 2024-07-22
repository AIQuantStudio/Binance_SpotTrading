from binance import Client


class Account:
    def __init__(self, name, apikey, secretkey):
        self.name = name
        self.apikey = apikey
        self.secretkey = secretkey
        
    def getAssetBalance(self, asset):
        binance_client = Client()
        balance = binance_client.get_asset_balance(asset='BTC')        