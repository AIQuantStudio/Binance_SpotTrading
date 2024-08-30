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
    M15 = "15m"
    M30 = "30m"
    HOUR = "1h"
    DAILY = "1d"
    WEEKLY = "1w"
    
    
    
class Trend(Enum):
    """"""
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
    CLOSETODAY = "平今"
    CLOSEYESTERDAY = "平昨"


class Status(Enum):
    """"""
    SUBMITTING = "提交中"
    NOTTRADED = "未成交"
    PARTTRADED = "部分成交"
    ALLTRADED = "全部成交"
    CANCELLED = "已撤销"
    REJECTED = "拒单"


class Product(Enum):
    """"""
    EQUITY = "股票"
    FUTURES = "期货"
    OPTION = "期权"
    INDEX = "指数"
    FOREX = "外汇"
    SPOT = "现货"
    ETF = "ETF"
    BOND = "债券"
    WARRANT = "权证"
    SPREAD = "价差"
    FUND = "基金"


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





class AppEngineMode(Enum):
    """"""
    BACKTESTING = "backtesting"
    SIMULATING = "simulating"
    TRADER = "trader"


class BacktestingMode(Enum):
    BAR = 1
    TICK = 2


class StopOrderStatus(Enum):
    WAITING = "等待中"
    CANCELLED = "已撤销"
    TRIGGERED = "已触发"
