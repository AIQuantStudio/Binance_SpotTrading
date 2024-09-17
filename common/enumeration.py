from enum import Enum


class EmptyEnum(Enum):
    NONE = ""

class TradeMode(Enum):
    EMPTY = 0
    TRADER = 1
    BACKTESTER = 2
    

class TradingDecision(Enum):
    EMPTY = 0
    BUY = 1
    SELL = 2
    
class Interval(Enum):
    MINUTE = "1m"
    M5 = "5m"
    M15 = "15m"
    M30 = "30m"
    HOUR = "1h"
    DAILY = "1d"
    WEEKLY = "1w"
    

class Scaler(Enum):
    NORMALIZATION = "归一化"
    STANDARDIZATION = "标准化"

class Trend(Enum):
    RISE = "涨"
    FALL = "跌"
    
class Direction(Enum):
    """"""
    BUY = "多"
    SELL = "空"


class Offset(Enum):
    """"""
    NONE = ""
    OPEN = "开"
    CLOSE = "平"


class Status(Enum):
    """"""
    SUBMITTING = "提交中"
    NOTTRADED = "未成交"
    PARTTRADED = "部分成交"
    ALLTRADED = "全部成交"
    CANCELLED = "已撤销"
    REJECTED = "拒单"



class OrderType(Enum):
    """
    订单类型
    """
    LIMIT = "限价"
    MARKET = "市价"
    STOP = "STOP"
    FAK = "FAK"
    FOK = "FOK"
    RFQ = "询价"


class Exchange(Enum):
    """"""
    LOCAL = "LOCAL"
    BINANCE = "BINANCE"
    HUOBI = "HUOBI"
    OKEX = "OKEX"



class StopOrderStatus(Enum):
    WAITING = "等待中"
    CANCELLED = "已撤销"
    TRIGGERED = "已触发"
