import asyncio
from binance import Client
from binance import AsyncClient


class BinanceAccount:
    def __init__(self, name, apikey, secretkey):
        self.name = name
        self.apikey = apikey
        self.secretkey = secretkey

        asyncio.run(self.create_client())
        print("********************")

    async def create_client(self):
        print(self.apikey)
        print(self.secretkey)
        self.binance_client = await AsyncClient.create(api_key=self.apikey, api_secret=self.secretkey)
        print(self.binance_client)
        
    def getAssetBalance(self, asset):
        print(22222)
        
        # loop = asyncio.get_event_loop()
        # get_future = asyncio.ensure_future(self.async_get_asset_balance(asset)) # 相当于开启一个future
        # self.main_loop.run_until_complete(get_future) # 事件循环
        self.new_loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self.new_loop)
        task = asyncio.create_task(self.async_get_asset_balance(asset))
        self.new_loop.run_until_complete(asyncio.wait([task]))
        
        # self.new_loop = asyncio.new_event_loop()
        # asyncio.run(self.async_get_asset_balance(asset))
        
    
    async def async_get_asset_balance(self, asset):
        balance = await self.binance_client.get_asset_balance(asset=asset)
        print(balance)
        