from threading import Thread
from datetime import date, datetime, timedelta
from functools import lru_cache
import time

from main_engine import MainEngine
from model import ModelFactory
from common import TradeSettingStruct, LogStruct, BarStruct
from event import Event, EVENT_LOG
from exchange import BinanceMarket
from strategy import BaseStrategy
from common import Utils


class Backtester:
    
    def __init__(self, model_id, strategy:BaseStrategy, setting_data:TradeSettingStruct):
        self.model_id = model_id
        self.strategy : BaseStrategy = strategy

        self.backtest_setting_data: TradeSettingStruct = setting_data
        self._history_data = []
        
        self._preload_count = 32
        
        # self.model_id = model_id
        # self._backtesting: BacktesterEngine = BacktesterEngine(self.model_id)
        # self._thread = None
        
        # self.backtest_setting_data: BacktestSettingStruct = None
    
    # def init(self, data):
    #     self._backtesting = BacktesterEngine(data)
        
    
    def clear_data(self):
        self._history_data.clear()
        
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


    def run_strategy(self):
        print(self.strategy)
        print("=====================")
        self.strategy.on_init()

        count = 0
        ix = 0
        # 预处理数据
        print(len(self._history_data))
        print(self._preload_count)
        for ix, bar_data in enumerate(self._history_data):
            if count >= self._preload_count:
                break
            
            count += 1
            # self.datetime = bar_data.datetime

            try:
                bar = Utils.data_to_bar(self.strategy.symbol, self.strategy.interval, bar_data)
                # self._preload_callback(bar_data)
                self.strategy.preload(bar)
            except Exception:
                self.write_log("触发异常，回测终止")
                # self.write_log(traceback.format_exc())
                return

        # self.strategy.inited = True
        self.write_log("策略初始化完成")

        self.strategy.on_start()
        # self.strategy.trading = True
        self.write_log("开始回放历史数据")

        # 使用剩余的历史数据来运行回测
        for data in self._history_data[ix:]:
            try:
                bar = Utils.data_to_bar(self.strategy.symbol, self.strategy.interval, data)
                # print(bar)
                self.new_bar(bar)
                time.sleep(2)
                # break
            except Exception:
                self.write_log("触发异常，回测终止")
                # self.write_log(traceback.format_exc())
                return

        self.write_log("历史数据回放结束")
    
    def new_bar(self, bar: BarStruct):
        self.bar = bar
        self.datetime = bar.datetime

        self.strategy.on_bar(bar)

        # self.update_daily_close(bar.close_price)

    def resume(self):
        pass

    def stop(self):
        pass
    
    def close(self):
        pass
    
    def write_log(self, msg):
        MainEngine.write_log(msg)
        MainEngine.event_engine.put(event=Event(EVENT_LOG, LogStruct(msg=msg)), suffix=self.model_id)
        
        
@lru_cache(maxsize=999)
def load_bar_data(symbol: str, start: datetime, end: datetime, interval_delta:timedelta):
    with BinanceMarket() as market:
        data = market.load_klines(symbol, start, end, interval_delta)

    return data, data[-1][0]