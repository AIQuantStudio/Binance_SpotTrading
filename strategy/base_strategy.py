from abc import ABC, abstractmethod
from copy import copy
from typing import Any, Callable



from app_engine import AppEngine
from event import Event, EVENT_LOG
from structure import LogStruct, BarStruct, Interval


class BaseStrategy(ABC):
    """
    策略模板类

    app engine 对象需要实现以下方法：
    send_order()
    cancel_order()
    cancel_all()
    write_log()
    get_pricetick()
    load_bar()
    load_tick()
    send_email()
    sync_strategy_data()
    get_mode()
    """

    name = ""
    author = ""
    parameters = []
    variables = []

    def __init__(self, strategy_engine: StrategyInterface,  vt_symbol: str, setting: dict):
        self.strategy_engine = strategy_engine
        self.vt_symbol = vt_symbol

        self.inited = False
        self.trading = False
        self.pos = 0

        # 复制一份新的variables，防止多个策略对象竞争操作(variables为类属性，转化为对象属性)
        self.variables = copy(self.variables)
        self.variables.insert(0, "inited")
        self.variables.insert(1, "trading")
        self.variables.insert(2, "pos")

        self.update_parameters(setting)
    
    @abstractmethod
    def on_init(self):
        pass
    
    @abstractmethod
    def preload(self):
        pass
    
    
    def update_parameters(self, setting: dict):
        """"""
        for name in self.parameters:
            if name in setting:
                setattr(self, name, setting[name])

    @classmethod
    def get_class_parameters(cls):
        """"""
        class_parameters = {}
        for name in cls.parameters:
            class_parameters[name] = getattr(cls, name)
        return class_parameters

    def get_parameters(self):
        """"""
        strategy_parameters = {}
        for name in self.parameters:
            strategy_parameters[name] = getattr(self, name)
        return strategy_parameters

    def get_variables(self):
        """"""
        strategy_variables = {}
        for name in self.variables:
            strategy_variables[name] = getattr(self, name)
        return strategy_variables

    def get_data(self):
        """"""
        strategy_data = {
            "strategy_class_name": self.__class__.__name__,
            "strategy_name": self.name,
            "vt_symbol": self.vt_symbol,
            "author": self.author,
            "parameters": self.get_parameters(),
            "variables": self.get_variables(),
        }
        return strategy_data

    
    
    
    
    
    @Wrapper.virtual
    def on_start(self):
        """"""
        pass

    @Wrapper.virtual
    def on_stop(self):
        """"""
        pass

    @Wrapper.virtual
    def on_tick(self, tick: TickData):
        """"""
        pass

    @Wrapper.virtual
    def on_bar(self, bar: BarData):
        """"""
        pass

    @Wrapper.virtual
    def on_trade(self, trade: TradeData):
        """"""
        pass

    @Wrapper.virtual
    def on_order(self, order: OrderData):
        """"""
        pass

    @Wrapper.virtual
    def on_stoporder(self, stop_order: StoporderData):
        """"""
        pass

    def buy(self, price: float, volume: float, stop: bool = False, lock: bool = False):
        """
        买单或多单开单
        """
        return self.send_order(Direction.BUY, Offset.OPEN, price, volume, stop, lock)

    def sell(self, price: float, volume: float, stop: bool = False, lock: bool = False):
        """
        卖单或多单平仓
        """
        return self.send_order(Direction.SELL, Offset.CLOSE, price, volume, stop, lock)

    def short(self, price: float, volume: float, stop: bool = False, lock: bool = False):
        """
        空单开仓
        """
        return self.send_order(Direction.SELL, Offset.OPEN, price, volume, stop, lock)

    def cover(self, price: float, volume: float, stop: bool = False, lock: bool = False):
        """
        空单平仓
        """
        return self.send_order(Direction.BUY, Offset.CLOSE, price, volume, stop, lock)

    def send_order(self, direction: Direction, offset: Offset, price: float, volume: float, stop: bool = False, lock: bool = False):
        """"""
        if self.trading:
            vt_orderids = self.app_engine.send_order(direction, offset, price, volume, stop, lock)
            return vt_orderids
        else:
            return []

    def cancel_order(self, vt_order_id: str):
        """"""
        if self.trading:
            self.app_engine.cancel_order(vt_order_id)

    def cancel_all(self):
        """"""
        if self.trading:
            self.app_engine.cancel_all()

    def write_log(self, msg: str):
        """"""
        self.app_engine.write_log(msg)

    # def preload_backtest_bar(self, count: int, callback: Callable[[TickData], None] = None):
    #     """
    #     预加载历史K线数据
    #     """
    #     if self.app_engine.mode == AppEngineMode.BACKTESTING:
    #         if not callback:
    #             callback = self.on_bar

    #         self.app_engine.preload_bar(count, callback)

    def preload_bar(self, count: int,  callback: Callable[[BarStruct], None] = None, interval=Interval.MINUTE):
        """ 预加载历史K线数据 """
        if not callback:
            callback = self.on_bar

        self.strategy_engine.preload_bar(count, callback, interval)

    def load_tick(self, days: int):
        """
        为初始化策略加载历史切片数据
        """
        self.app_engine.load_tick(days, self.on_tick)

    def load_bar(self, days: int, interval: Interval = Interval.MINUTE, callback: Callable[[BarData], None] = None, use_database: bool = False):
        """
        为初始化策略加载历史K线数据
        """
        if not callback:
            callback = self.on_bar

        self.app_engine.load_bar(days, interval, callback, use_database)

    def get_pricetick(self):
        """
        返回合约的价格切片
        """
        return self.app_engine.get_pricetick()

    def send_email(self, msg):
        """
        发送邮件
        """
        if self.inited:
            self.app_engine.send_email(msg)

    def update_strategy_status(self):
        """"""
        if self.inited:
            if self.app_engine.mode == AppEngineMode.TRADER:
                event = {
                    "type": "update_trading_controller",
                    "data": self.app_engine.name,
                }
                self.app_engine.put_strategy_event(event)

    # def sync_data(self):
    #     """
    #     同步策略变量数据，保存到磁盘
    #     """
    #     if self.trading:
    #         self.app_engine.sync_strategy_data(self)

    # def engine_mode(self):
    #     """
    #     返回当前服务状态(回测，实盘)
    #     """
    #     return self.app_engine.get_mode()

    def write_log(self, msg):
        AppEngine.write_log(msg)
        AppEngine.event_engine.put(event=Event(EVENT_LOG, LogStruct(msg=msg)), suffix=self.model_id)