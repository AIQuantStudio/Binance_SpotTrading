from binance import Client


class BinanceAccount:
    
    def __init__(self):
        self.name
        self.id
        self.api_key = ""
        self.api_secret = ""
        
    def connect(self):
        try:
            self.client = Client(self.api_key, self.api_secret)
            info = self.client.get_account()
        except:
            self.client = None
            return False
        
        return True