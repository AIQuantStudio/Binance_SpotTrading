import pandas as pd
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import mplfinance as mpf
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.figure import Figure
from PyQt6.QtWidgets import *

matplotlib.use("QtAgg")

plt.rcParams["axes.unicode_minus"] = False

STYLE_DICT = {"xtick.color": "white", "ytick.color": "white", "xtick.labelcolor": "white", "ytick.labelcolor": "white", "axes.spines.top": False, "axes.spines.right": False, "axes.labelcolor": "white"}


class MarketFigure(FigureCanvasQTAgg):

    def __init__(self, width=12, height=8, dpi=100):
        self.predict_price = None

        mcolors = mpf.make_marketcolors(up="green", down="red", edge="in", wick="in")
        my_style = mpf.make_mpf_style(base_mpf_style="binance", marketcolors=mcolors, facecolor="#19232D", figcolor="#111111", rc=STYLE_DICT)
        self.fig = Figure(figsize=(width, height), dpi=dpi, facecolor='#333', edgecolor='black')

        self.axes = self.fig.add_subplot(111)
        self.axes.set_facecolor('#333')

        super(MarketFigure, self).__init__(self.fig)
        
    def plot_data(self, data):
        df = pd.DataFrame(data, columns=["datetime", "Open", "High", "Low", "Close", "Volume", "CloseTime", "QuoteVolume", "NumberTrades", "BuyBaseVolume", "BuyQuoteVolume", "Ignored"], dtype=float)
        df["datetime"] = pd.to_datetime(df["datetime"] / 1000.0, unit="s")
        # df.set_index("datetime", inplace=True)
        self.axes.set_xlabel('time')
        self.axes.set_ylabel('number')
        
        self.axes.plot(df["datetime"], df["Close"],color = 'r')

        self.draw()

    def set_predict_price(self, price):
        self.predict_price = price
