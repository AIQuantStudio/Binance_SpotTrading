import asyncio
from datetime import date, datetime, timedelta
from PyQt6.QtCore import QTimer

from binance import Client


class BinanceMarket:
    def __init__(self):
        # self.symbol = pair
        self.binance_client = Client()

    def get_last_klines(self, symbol):
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

        data = self.binance_client.get_klines(symbol=symbol, interval=Client.KLINE_INTERVAL_15MINUTE, limit=200)
        # print(data)
        return data

    def load_klines(self, symbol, start_datetime: datetime, end_datetime: datetime, interval_delta: timedelta):
        result = []
        start = start_datetime
        while start < end_datetime:
            data = self.binance_client.get_klines(symbol=symbol, interval=Client.KLINE_INTERVAL_15MINUTE, limit=6, startTime=int(start.timestamp() * 1000), endTime=int(end_datetime.timestamp() * 1000))

            start = datetime.fromtimestamp(data[-1][0] / 1000.0) + interval_delta
            result = result + data

        return result

    def __enter__(self):
        self.binance_client = Client()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.binance_client.close_connection()
