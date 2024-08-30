from typing import Tuple
from decimal import Decimal
from math import floor, ceil
from datetime import datetime

from structure import BarStruct


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
