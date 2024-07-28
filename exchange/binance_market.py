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
        
    def get_klines(self, symbol, interval, limit, start_time, end_time):
        """Kline/candlestick bars for a symbol. Klines are uniquely identified by their open time.

        https://binance-docs.github.io/apidocs/spot/en/#kline-candlestick-data

        :param symbol: required
        :type symbol: str
        :param interval: -
        :type interval: str
        :param limit: - Default 500; max 1000.
        :type limit: int
        :param startTime:
        :type startTime: int
        :param endTime:
        :type endTime: int

        :returns: API response

        .. code-block:: python

            [
                [
                    1499040000000,      # Open time
                    "0.01634790",       # Open
                    "0.80000000",       # High
                    "0.01575800",       # Low
                    "0.01577100",       # Close
                    "148976.11427815",  # Volume
                    1499644799999,      # Close time
                    "2434.19055334",    # Quote asset volume
                    308,                # Number of trades
                    "1756.87402397",    # Taker buy base asset volume
                    "28.46694368",      # Taker buy quote asset volume
                    "17928899.62484339" # Can be ignored
                ]
            ]

        :raises: BinanceRequestException, BinanceAPIException

        """
        
        data = self.binance_market.get_klines(symbol, interval, limit, start_time, end_time)
        