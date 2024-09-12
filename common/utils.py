from typing import Tuple
from decimal import Decimal
from math import floor, ceil
from datetime import datetime, timedelta

from structure import BarStruct, Interval

def _convert_interval(str_interval:str):
    if str_interval == "1m" or str_interval == "1M":
        return Interval.MINUTE
    elif str_interval == "5m" or str_interval == "5M":
        return Interval.M5
    elif str_interval == "15m" or str_interval == "15M":
        return Interval.M15
    elif str_interval == "30m" or str_interval == "30M":
        return Interval.M30
    elif str_interval == "1h" or str_interval == "1H":
        return Interval.HOUR
    elif str_interval == "1d" or str_interval == "1D":
        return Interval.DAILY
    elif str_interval == "1w" or str_interval == "1W":
        return Interval.WEEKLY

def _interval_to_timedelta(interval:Interval):
    if interval == Interval.MINUTE:
        return timedelta(minutes=1)
    elif interval == Interval.M5:
        return timedelta(minutes=5)
    elif interval == Interval.M15:
        return timedelta(minutes=15)
    elif interval == Interval.M30:
        return timedelta(minutes=30)
    elif interval == Interval.HOUR:
        return timedelta(hours=1)
    elif interval == Interval.DAILY:
        return timedelta(days=1)
    elif interval == Interval.WEEKLY:
        return timedelta(days=7)
    
def _data_to_bar(symbol, interval, data: list) -> BarStruct:
    dt = datetime.fromtimestamp(data[0]/1000.0)
    open = data[1]
    high = data[2]
    low = data[3]
    close = data[4]
    volume = data[5]
    trades = data[8]

    return BarStruct(symbol=symbol, interval=interval, datetime=dt, open_price=open, high_price=high, low_price=low, close_price=close, volume=volume, trades=trades)

def _timestamp_array_to_datetime_array(timestamp_array:list, unix = False):
    datetime_array = []
    div = 1 if unix else 1000.0
    for timestamp in timestamp_array:
        timestamp = float(timestamp)
        d = datetime.fromtimestamp(timestamp/div)
        datetime_array.append(d)
    return datetime_array


# 导出 Utils
class Utils:
    data_to_bar = _data_to_bar
    convert_interval = _convert_interval
    interval_to_timedelta = _interval_to_timedelta
    timestamp_array_to_datetime_array = _timestamp_array_to_datetime_array

