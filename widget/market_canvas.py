from PyQt6.QtCore import *
from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
import pandas as pd
import numpy as np

from widget.market_figure import MarketFigure

from model import ModelFactory
from exchange import BinanceMarket
from main_engine import MainEngine


class MarketCanvas(QFrame):

    def __init__(self, parent_widget, app_id):
        super().__init__(parent_widget)
        
        self.app_id = app_id
        self.symbol = ModelFactory().get_model_symbol(self.app_id)

        self.setLineWidth(2)
        self.setMidLineWidth(2)
        self.setFrameStyle(QFrame.Shape.Panel | QFrame.Shadow.Raised)
        # self.setStyleSheet("background-color:#2a2a2a")
        
        self.last_high = QLabel("1")
        self.last_low = QLabel("2")
        self.last_close = QLabel("3")
        self.last_volume = QLabel("4")
        self.predict_price = QLabel("5")
        
        vbox_layout = QVBoxLayout(self)
        grid = QGridLayout()
        grid.addWidget(QLabel("最高价"), 0, 0, Qt.AlignmentFlag.AlignRight)
        grid.addWidget(QLabel("最低价"), 1, 0, Qt.AlignmentFlag.AlignRight)
        grid.addWidget(QLabel("成交价"), 0, 2,Qt.AlignmentFlag.AlignRight)
        grid.addWidget(QLabel("交易量"), 1, 2,Qt.AlignmentFlag.AlignRight)
        grid.addWidget(QLabel("预测价格"), 0, 4,Qt.AlignmentFlag.AlignRight)
        grid.addWidget(self.last_high, 0, 1,Qt.AlignmentFlag.AlignLeft)
        grid.addWidget(self.last_low, 1, 1,Qt.AlignmentFlag.AlignLeft)
        grid.addWidget(self.last_close, 0, 3,Qt.AlignmentFlag.AlignLeft)
        grid.addWidget(self.last_volume, 1, 3,Qt.AlignmentFlag.AlignLeft)
        grid.addWidget(self.predict_price, 0, 5,Qt.AlignmentFlag.AlignLeft)
        
        grid.setColumnStretch(0,1)
        grid.setColumnStretch(1,6)
        grid.setColumnStretch(2,1)
        grid.setColumnStretch(3,6)
        grid.setColumnStretch(4,1)
        grid.setColumnStretch(5,4)
        vbox_layout.addLayout(grid)

        self.market_figure = MarketFigure()
        vbox_layout.addWidget(self.market_figure)
        
        self.setLayout(vbox_layout)
        

    def start_market(self):
        MainEngine.event_engine.register_timer(self.refresh_cline, interval=1)
        
    def stop_market(self):
        MainEngine.event_engine.unregister_timer(self.refresh_cline)
        
    def refresh_cline(self):
        data = BinanceMarket().get_last_klines(self.symbol)
        
        # df = pd.DataFrame(data, columns=["datetime", "Open", "High", "Low", "Close", "Volume", "CloseTime", "QuoteVolume", "NumberTrades", "BuyBaseVolume", "BuyQuoteVolume", "Ignored"], dtype=float)
        # df["datetime"] = pd.to_datetime(df["datetime"] / 1000.0, unit="s")
        
        
        self.market_figure.plot_data(data)
        
    def set_predict_price(self, price):
        self.predict_price.setText(str(price))
        