from abc import ABC
from typing import Callable

from harvester.main_engine import MainEngine
from harvester.enumeration import Direction, Interval, Offset, AppEngineMode
from harvester.structure import TickData, BarData
from harvester.common import Wrapper

from structure import Interval


class StrategyInterface(ABC):

    def __init__(self, model_id, mode: TradeMode):
        # self.main_engine = main_engine
        self.mode = mode

    @Wrapper.virtual
    def preload_bar(self, count: int, callback: Callable[[BarStruct], None], interval: Interval):
        pass

    # @Wrapper.virtual
    # def load_tick(self, days: int, callback: Callable[[TickData], None]):
    #     """"""
    #     pass

    # @Wrapper.virtual
    # def load_bar(self, count: int, interval: Interval, callback: Callable[[BarData], None]):
    #     """"""
    #     pass

    @Wrapper.virtual
    def get_pricetick(self):
        """"""
        pass

    @Wrapper.virtual
    def send_order(self, direction: Direction, offset: Offset, price: float, volume: float, stop: bool, lock: bool):
        """"""
        pass

    @Wrapper.virtual
    def cancel_order(self, vt_order_id: str):
        """"""
        pass

    @Wrapper.virtual
    def cancel_all(self):
        """"""
        pass

    @Wrapper.virtual
    def send_email(self, msg: str):
        """"""
        pass

    @Wrapper.virtual
    def write_log(self, msg: str):
        """"""
        pass

    @Wrapper.virtual
    def put_strategy_event(self, data: dict):
        """"""
        pass
