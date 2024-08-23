from PyQt6.QtCore import *
from functools import lru_cache
from datetime import date, datetime, timedelta
import time

from app_engine import AppEngine
from model import ModelFactory
from structure import TestSettingStruct, LogStruct
from event import Event, EVENT_LOG
from exchange import BinanceMarket


class BacktesterEngine:

    def __init__(self, model_id, strategy, setting_data):
        self.model_id = model_id
        self.strategy : BaseStrategy = strategy

        self.backtest_setting_data: TestSettingStruct = setting_data
        self._history_data = []

    def clear_data(self):
        self._history_data.clear()
        # self._result_df = None
        # self._result_statistics = None
        # self._result_values = None

        # self.strategy = None
        # self.tick = None
        # self.bar = None
        # self.datetime = None

        # self.stop_order_count = 0
        # self.stop_orders.clear()
        # self.active_stop_orders.clear()

        # self.limit_order_count = 0
        # self.limit_orders.clear()
        # self.active_limit_orders.clear()

        # self.trade_count = 0
        # self.trades.clear()

        # self.logs.clear()
        # self.daily_results.clear()

    def load_history_data(self):
        self.write_log("开始加载历史数据")

        if not self.backtest_setting_data.end_datetime:
            self.backtest_setting_data.end_datetime = datetime.now()

        if self.backtest_setting_data.begin_datetime >= self.backtest_setting_data.end_datetime:
            self.write_log("起始日期必须小于结束日期")
            return

        self._history_data.clear()

        progress_delta = timedelta(hours=4)
        interval_delta = timedelta(minutes=15)

        total_delta = self.backtest_setting_data.end_datetime - self.backtest_setting_data.begin_datetime
        start = self.backtest_setting_data.begin_datetime
        end = self.backtest_setting_data.begin_datetime + progress_delta
        progress = 0

        while start < self.backtest_setting_data.end_datetime:
            end = min(end, self.backtest_setting_data.end_datetime)

            data, data_end_time = load_bar_data(ModelFactory().get_model_symbol(self.model_id), start, end, interval_delta)
            
  
            self._history_data.extend(data)

            progress += progress_delta / total_delta
            progress = min(progress, 1)
            progress_bar = "#" * int(progress * 10)
            self.write_log(f"加载进度：{progress_bar} [{progress:.0%}]")

            start = datetime.fromtimestamp(data_end_time/1000.0) + interval_delta
            end += (progress_delta + interval_delta)

        self.write_log(f"历史数据加载完成，数据量：{len(self._history_data)}")

    def run_backtesting(self):
        self.strategy.on_init()

        count = 0
        ix = 0
        # 预处理数据
        for ix, data in enumerate(self._history_data):
            if count >= self._preload_count:
                break

            count += 1
            self.datetime = data.datetime

            try:
                self._preload_callback(data)
            except Exception:
                self.write_log("触发异常，回测终止")
                # self.write_log(traceback.format_exc())
                return

        self.strategy.inited = True
        self.write_log("策略初始化完成")

        self.strategy.on_start()
        self.strategy.trading = True
        self.write_log("开始回放历史数据")

        # 使用剩余的历史数据来运行回测
        for data in self._history_data[ix:]:
            try:
                self._new_bar(data)
            except Exception:
                self.write_log("触发异常，回测终止")
                # self.write_log(traceback.format_exc())
                return

        self.write_log("历史数据回放结束")

    def new_bar(self, bar: BarStruct):
        self.bar = bar
        self.datetime = bar.datetime

        self.strategy.on_bar(bar)

        self.update_daily_close(bar.close_price)
        
    def write_log(self, msg):
        AppEngine.write_log(msg)
        AppEngine.event_engine.put(event=Event(EVENT_LOG, LogStruct(msg=msg)), suffix=self.model_id)


    def send_order(self, strategy: BaseStrategy, direction: Direction, offset: Offset, price: float, volume: float, stop: bool, lock: bool):
        """"""
        price = Utils.round_to(price, self._pricetick)
        if stop:
            vt_order_id = self.send_stop_order(direction, offset, price, volume)
        else:
            vt_order_id = self.send_limit_order(direction, offset, price, volume)
        return [vt_order_id]

@lru_cache(maxsize=999)
def load_bar_data(symbol: str, start: datetime, end: datetime, interval_delta:timedelta):
    with BinanceMarket() as market:
        data = market.load_klines(symbol, start, end, interval_delta)

    return data, data[-1][0]
