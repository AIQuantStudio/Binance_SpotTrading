import asyncio

from PyQt6.QtCore import QTimer

from binance import Client
from binance import AsyncClient


class BinanceMarket:
    def __init__(self, pair):
        self.symbol = pair
        self.binance_market = Client()
        
        self.worker = MarketWorker()
        

    def get_order_book(self, symbol):
        self.timer = QTimer()
        self.timer.timeout.connect(self.async_get_order_book)
        self.timer.start()
        
        asyn = AsyncMarket(self.async_get_asset_balance)
        asyn.start()
        
        
        # loop = asyncio.get_event_loop()
        # get_future = asyncio.ensure_future(self.async_get_asset_balance(asset)) # 相当于开启一个future
        # self.main_loop.run_until_complete(get_future) # 事件循环
        self.new_loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self.new_loop)
        task = asyncio.create_task(self.async_get_asset_balance(asset))
        self.new_loop.run_until_complete(asyncio.wait([task]))
        
        # self.new_loop = asyncio.new_event_loop()
        # asyncio.run(self.async_get_asset_balance(asset))
        
    def async_get_order_book(self):
        balance = self.binance_market.get_asset_balance(asset=asset)
        print(balance)
        
        result = ...
        AsyncMarket.signals.result.emit(result)
        
    async def async_get_asset_balance(self, asset):
        