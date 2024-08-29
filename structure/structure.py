from PyQt6.QtCore import *
from dataclasses import dataclass
from datetime import datetime as dt
from logging import INFO

from structure.enumeration import Interval, TradeMode


@dataclass
class AssetBalanceData:

    currency: str = ""
    free: float = 0
    locked: float = 0

    def __post_init__(self):
        self.total = self.free + self.locked


@dataclass
class BianceAccountData:

    name: str
    id: str
    api_key: str
    secret_key: str


@dataclass
class BianceTestAccountData:

    name: str
    id: str
    db: str


@dataclass
class TradeSettingStruct:
    mode: TradeMode.EMPTY
    predict_at_first_time: bool
    begin_datetime: dt
    end_datetime: dt
    refer_currency: str
    trade_amount: float
    strategy_name: str
    
    def __post_init__(self):
        if self.mode == TradeMode.BACKTEST:
            pass


@dataclass
class LogStruct:
    msg: str
    level: int = INFO

    def __post_init__(self):
        self.time = dt.now()


@dataclass
class BarStruct:
    symbol: str
    interval: Interval = None

    datetime: dt = None
    open_price: float = 0
    high_price: float = 0
    low_price: float = 0
    close_price: float = 0
    volume: float = 0
