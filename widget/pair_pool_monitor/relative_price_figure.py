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


class RelativePriceFigure(FigureCanvasQTAgg):

    def __init__(self, width=12, height=8, dpi=100):
        # self.predict_price = None

        # mcolors = mpf.make_marketcolors(up="green", down="red", edge="in", wick="in")
        # my_style = mpf.make_mpf_style(base_mpf_style="binance", marketcolors=mcolors, facecolor="#19232D", figcolor="#111111", rc=STYLE_DICT)
        self.fig = Figure(figsize=(width, height), dpi=dpi, facecolor='#333', edgecolor='black')

        self.axes = self.fig.add_subplot(111)
        self.axes.set_facecolor('#333')
        self.axes.set_xlabel('time')
        self.axes.set_ylabel('price')

        super(RelativePriceFigure, self).__init__(self.fig)
        
    # def plot_data(self, data):
    #     df = pd.DataFrame(data, columns=["datetime", "Open", "High", "Low", "Close", "Volume", "CloseTime", "QuoteVolume", "NumberTrades", "BuyBaseVolume", "BuyQuoteVolume", "Ignored"], dtype=float)
    #     df["datetime"] = pd.to_datetime(df["datetime"] / 1000.0, unit="s")
    #     # df.set_index("datetime", inplace=True)
        
    #     self.axes.plot(df["datetime"], df["Close"],color = 'r')

    #     self.draw()
        
    # def plot(self, close_df, predict_df):
    #     self.axes.plot(close_df["datetime"], close_df["Close"], color = 'r')
    #     if predict_df is not None:
    #         self.axes.plot(predict_df["datetime"], predict_df["Close"], color = 'g')
            
    def plot_multi_line(self, data):
        for d in data:
            name = d["name"]
            x = d["x"]
            y = d["y"]
            self.axes.plot(x, y, label = name)
            
        self.axes.legend()
        