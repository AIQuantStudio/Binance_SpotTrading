from PyQt6.QtCore import *
from dataclasses import dataclass
from datetime import datetime as dt
from logging import INFO

from common.enumeration import Interval, TradeMode, OrderType, Direction, Offset, Status


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
        if self.mode == TradeMode.BACKTESTER:
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
    trades: int = 0


@dataclass
class OrderStruct:

    symbol: str
    order_id: str

    type: OrderType = OrderType.LIMIT
    direction: Direction = None
    offset: Offset = Offset.NONE
    price: float = 0
    volume: float = 0
    traded: float = 0
    status: Status = Status.SUBMITTING
    datetime: dt = None

    def is_active(self) -> bool:
        if self.status in [Status.SUBMITTING, Status.NOTTRADED, Status.PARTTRADED]:
            return True
        else:
            return False



@dataclass
class StoporderData:
    """"""
    vt_symbol: str
    direction: Direction
    offset: Offset
    price: float
    volume: float
    stoporder_id: str
    strategy_name: str
    lock: bool = False
    vt_order_ids: list = field(default_factory=list)
    status: StopOrderStatus = StopOrderStatus.WAITING
        
        
@dataclass
class ContractStruct:
    
    symbol: str
    name: str
    size: int
    pricetick: float

    min_volume: float = 1           # 合同最小交易量
    stop_supported: bool = False    # 服务器是否支持停止命令
    net_position: bool = False      # 是否使用净持仓量表示
    history_data: bool = False      # 是否提供历史数据
