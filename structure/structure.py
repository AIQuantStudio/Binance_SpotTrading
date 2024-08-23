from PyQt6.QtCore import *
from dataclasses import dataclass
from datetime import datetime
from logging import INFO

from structure.enumeration import Interval


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
class TestSettingStruct:
    
    predict_at_first_time: bool
    begin_datetime: datetime
    end_datetime: datetime
    refer_currency: str
    trade_amount: float
    
    
@dataclass
class LogStruct:
    msg: str
    level: int = INFO

    def __post_init__(self):
        self.time = datetime.now()
        

@dataclass
class BarStruct:
    symbol: str
    interval: Interval = None
    
    datetime: datetime
    open_price: float = 0
    high_price: float = 0
    low_price: float = 0
    close_price: float = 0
    volume: float = 0


