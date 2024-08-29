from datetime import datetime
from collections import OrderedDict
from typing import Any, Dict

from strategy.base_strategy import BaseStrategy

from structure import BarStruct


class SimpleStrategy(BaseStrategy):

    def __init__(self, app_id):
        super().__init__(app_id)

        self.history_bar: OrderedDict[datetime, BarStruct] = {}
        self.history_predict: OrderedDict[datetime, float] = {}

        self.last_bar :BarStruct = None
        self.last_predict_price:float = 0
        self.last_predict_datetime:datetime = None
        
        
        self.bar_gen = BarGenerator(self.on_bar)
        self.bar_serial = BarSerial()

    def on_init(self):
        """ 重写 BaseStrategy::on_init """
        self.write_log("策略初始化")

        self.rsi_buy = 50 + self.rsi_entry
        self.rsi_sell = 50 - self.rsi_entry

        self.preload_bar(10)
        # self.load_bar(10)
        
    def preload(self, bar: BarStruct):
        """ 重写 BaseStrategy::preload """
        self.history_bar[bar.datetime] = bar

    def on_start(self):
        """ 重写 BaseStrategy::on_start """
        self.write_log("策略启动")

    def on_stop(self):
        """ 重写 BaseStrategy::on_stop """
        self.write_log("策略停止")
        
    def on_bar(self, bar: BarStruct):
        """ 重写 BaseStrategy::on_bar """
        self.last_bar = bar

        # 根据最近的历史Bar来预测价格
        cur_predict_price, cur_predict_datetime = ...
        
        if cur_predict_price > self.last_close_price:
            self.buy(bar.close_price, self.fixed_size)
        elif cur_predict_price > self.last_close_price:
            self.sell(bar.close_price, self.fixed_size)
        
        
        
        
        self.cancel_all()

        bs = self.bar_serial
        bs.update_bar(bar)
        if not bs.inited:
            return

        atr_array = bs.atr(self.atr_length, array=True)
        self.atr_value = atr_array[-1]
        self.atr_ma = atr_array[-self.atr_ma_length :].mean()
        self.rsi_value = bs.rsi(self.rsi_length)

        if self.pos == 0:
            self.intra_trade_high = bar.high_price
            self.intra_trade_low = bar.low_price

            if self.atr_value > self.atr_ma:
                if self.rsi_value > self.rsi_buy:
                    self.buy(bar.close_price + 5, self.fixed_size)
                elif self.rsi_value < self.rsi_sell:
                    self.short(bar.close_price - 5, self.fixed_size)

        elif self.pos > 0:
            self.intra_trade_high = max(self.intra_trade_high, bar.high_price)
            self.intra_trade_low = bar.low_price

            long_stop = self.intra_trade_high * (1 - self.trailing_percent / 100)
            self.sell(long_stop, abs(self.pos), stop=True)

        elif self.pos < 0:
            self.intra_trade_high = bar.high_price
            self.intra_trade_low = min(self.intra_trade_low, bar.low_price)

            short_stop = self.intra_trade_low * (1 + self.trailing_percent / 100)
            self.cover(short_stop, abs(self.pos), stop=True)

        self.put_event()
