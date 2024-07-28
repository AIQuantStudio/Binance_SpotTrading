import mplfinance as mpf
import pandas as pd
import matplotlib as mpl

mpl.use("QtAgg")
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from PyQt6.QtWidgets import *
import sys
from matplotlib.animation import FuncAnimation


class BinanceFigure(FigureCanvas):
    def __init__(self, width=12, height=8, dpi=100):
        mcolors = mpf.make_marketcolors(up="green", down="red", edge="in", wick="in", volume="in")
        my_style = mpf.make_mpf_style(base_mpf_style="binance", marketcolors=mcolors, facecolor="#19232D", mavcolors=["blue", "red", "yellow"])

        self.fig = mpf.figure(style=my_style, figsize=(width, height), dpi=dpi)
        super(BinanceFigure, self).__init__(self.fig)
        self.df = pd.read_csv("./data/SPY_20110701_20120630_Bollinger.csv", index_col=0, parse_dates=True)
        self.fig.subplots_adjust(left=0, bottom=0, right=1, top=0.95, hspace=0)
        self.ax1, self.ax2 = self.fig.subplots(nrows=2, ncols=1, sharex=True)
        mpf.plot(self.df.head(50), ax=self.ax1, type="candle", volume=self.ax2, mav=[5, 10, 30], axtitle="customize plot", tight_layout=True)
