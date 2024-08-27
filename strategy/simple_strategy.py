from datetime import datetime
from collections import OrderedDict
from typing import Any, Dict

from ..base import BaseStrategy
from harvester.structure import TickData, BarData, TradeData, OrderData, StoporderData
from harvester.common import BarGenerator, BarSerial

from structure import BarStruct


class AtrRsiStrategy(BaseStrategy):
    """"""

    name = "AtrRsiStrategy"
    author = "用Python的交易员"

    refer_currency = 22
    trade_amount = 10


    atr_value = 0
    atr_ma = 0
    rsi_value = 0
    rsi_buy = 0
    rsi_sell = 0
    intra_trade_high = 0
    intra_trade_low = 0

    parameters = ["refer_currency", "trade_amount"]
    variables = ["atr_value", "atr_ma", "rsi_value", "rsi_buy", "rsi_sell", "intra_trade_high", "intra_trade_low"]

    def __init__(self, engine: Any, vt_symbol: str, setting: Dict):
        super().__init__(engine, vt_symbol, setting)

        self.history_bar: OrderedDict[datetime, BarStruct] = {}
        self.history_predict: OrderedDict[datetime, float] = {}

        self.last_bar :BarData = None
        self.last_predict_price:float = 0
        self.last_predict_datetime:datetime = None
        
        
        self.bar_gen = BarGenerator(self.on_bar)
        self.bar_serial = BarSerial()

    def on_init(self):
        """重写 BaseStrategy::on_init"""
        self.write_log("策略初始化")

        self.rsi_buy = 50 + self.rsi_entry
        self.rsi_sell = 50 - self.rsi_entry

        self.preload_bar(10)
        # self.load_bar(10)
        
    def preload(self, bar: BarStruct):
        """重写 BaseStrategy::preload"""
        self.history_bar[bar.datetime] = bar

    def on_start(self):
        """重写 BaseStrategy::on_start"""
        self.write_log("策略启动")

    def on_stop(self):
        """重写 BaseStrategy::on_stop"""
        self.write_log("策略停止")

    def on_tick(self, tick: TickData):
        """重写 BaseStrategy::on_tick"""
        self.bar_gen.update_tick(tick)

    def on_bar(self, bar: BarData):
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

    def on_trade(self, trade: TradeData):
        """重写 BaseStrategy::on_trade"""
        self.put_event()

    def on_order(self, order: OrderData):
        """重写 BaseStrategy::on_order"""
        pass

    def on_stoporder(self, stop_order: StoporderData):
        """重写 BaseStrategy::on_stoporder"""
        pass
