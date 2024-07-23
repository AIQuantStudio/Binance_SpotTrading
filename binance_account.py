from binance import Client


class BinanceAccount:
    def __init__(self, name, apikey, secretkey):
        self.name = name
        self.apikey = apikey
        self.secretkey = secretkey
        
    def getAssetBalance(self, asset):
        binance_client = Client(api_key=self.apikey, api_secret=self.secretkey)
        balance = binance_client.get_asset_balance(asset=asset)
        print(balance)