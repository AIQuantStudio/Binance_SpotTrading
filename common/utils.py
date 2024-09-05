from typing import Tuple
from decimal import Decimal
from math import floor, ceil
from datetime import datetime

from structure import BarStruct, Interval

def _convert_interval(str_interval:str):
    if str_interval == "1m" and str_interval == "1M":
        return Interval.MINUTE
    elif str_interval == "5m" and str_interval == "5M":
        return Interval.M5
    elif str_interval == "15m" and str_interval == "15M":
        return Interval.M15
    elif str_interval == "30m" and str_interval == "30M":
        return Interval.M30
    elif str_interval == "1h" and str_interval == "1H":
        return Interval.HOUR
    elif str_interval == "1d" and str_interval == "1D":
        return Interval.DAILY
    elif str_interval == "1w" and str_interval == "1W":
        return Interval.WEEKLY

def _data_to_bar(symbol, interval, data: list) -> BarStruct:
    dt = datetime.fromtimestamp(data[0]/1000.0)
    open = data[1]
    high = data[2]
    low = data[3]
    close = data[4]
    volume = data[5]
    trades = data[8]

    return BarStruct(symbol=symbol, interval=interval, datetime=dt, open_price=open, high_price=high, low_price=low, close_price=close, volume=volume, trades=trades)


# 导出 Utils
class Utils:
    data_to_bar = _data_to_bar
    convert_interval = _convert_interval

