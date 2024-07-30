import mplfinance as mpf
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np


import matplotlib 


matplotlib.use("QtAgg")
matplotlib.rcParams['font.sans-serif'] = ['SimHei']
matplotlib.rcParams['axes.unicode_minus'] = False
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from PyQt6.QtWidgets import *
import sys
from matplotlib.animation import FuncAnimation


# plt.rcParams['font.sans-serif'] = ['SimHei']
# plt.rcParams['axes.unicode_minus'] = False



class BinanceFigure(FigureCanvas):
    
    def __init__(self, width=12, height=8, dpi=100):
        # mcolors = mpf.make_marketcolors(up="green", down="red", edge="in", wick="in", volume="in")
        # my_style = mpf.make_mpf_style(base_mpf_style="binance", marketcolors=mcolors, facecolor="#19232D", mavcolors=["blue", "red", "yellow"])

        # self.fig = mpf.figure(style=my_style, figsize=(width, height), dpi=dpi)
        # super(BinanceFigure, self).__init__(self.fig)
        # self.df = pd.read_csv("./data/SPY_20110701_20120630_Bollinger.csv", index_col=0, parse_dates=True)
        # self.fig.subplots_adjust(left=0, bottom=0, right=1, top=0.95, hspace=0)
        # self.ax1, self.ax2 = self.fig.subplots(nrows=2, ncols=1, sharex=True)
        # mpf.plot(self.df.head(50), ax=self.ax1, type="candle", volume=self.ax2, mav=[5, 10, 30], axtitle="customize plot", tight_layout=True)
        

        

        mcolors = mpf.make_marketcolors(up="green", down="red", edge="in", wick="in")
        my_style = mpf.make_mpf_style(base_mpf_style="binance", marketcolors=mcolors, facecolor="#19232D")
        self.fig = mpf.figure(style=my_style, figsize=(width, height), dpi=dpi)
        super(BinanceFigure, self).__init__(self.fig)
        
        # self.df = pd.read_csv("./data/SPY_20110701_20120630_Bollinger.csv", index_col=0, parse_dates=True)
        # print(self.df)
        
        # last_data = self.df.iloc[-1]
        
        
        # # 添加三个图表，四个数字分别代表图表左下角在figure中的坐标，以及图表的宽（0.88）、高（0.60）
        # ax1 = fig.add_axes([0.06, 0.25, 0.88, 0.60])
        # # 添加第二、三张图表时，使用sharex关键字指明与ax1在x轴上对齐，且共用x轴
        # # ax2 = fig.add_axes([0.06, 0.15, 0.88, 0.10], sharex=ax1)
        # # ax3 = fig.add_axes([0.06, 0.05, 0.88, 0.10], sharex=ax1)
        # # 设置三张图表的Y轴标签
        # ax1.set_ylabel('price')
        # # ax2.set_ylabel('volume')
        # # ax3.set_ylabel('macd')
        # # 在figure对象上添加文本对象，用于显示各种价格和标题
        # fig.text(0.50, 0.94, '513100.SH - 纳指ETF:')
        # fig.text(0.12, 0.90, '开/收: ')
        # fig.text(0.14, 0.89, f'{np.round(last_data["Open"], 3)} / {np.round(last_data["Close"], 3)}')
        # fig.text(0.12, 0.86, f'{last_data.name.date()}')
        # fig.text(0.40, 0.90, '高: ')
        # fig.text(0.40, 0.90, f'{last_data["High"]}')
        # fig.text(0.40, 0.86, '低: ')
        # fig.text(0.40, 0.86, f'{last_data["Low"]}')
        # fig.text(0.55, 0.90, '量(万手): ')
        # fig.text(0.55, 0.90, f'{np.round(last_data["Volume"] / 10000, 3)}')
        # fig.text(0.70, 0.90, '涨停: ')
        # fig.text(0.70, 0.90, f'{last_data["UpperB"]}')
        # fig.text(0.70, 0.86, '跌停: ')
        # fig.text(0.70, 0.86, f'{last_data["LowerB"]}')
        
        # self.df.loc[:,'Open'] = 0
        # self.df.loc[:,'Close'] = 0
        # self.df.loc[:,'High'] = 0
        # self.df.loc[:,'Low'] = 0
        # self.df.loc[:,'Volume'] = 0

        
        
        
        # # 调用mpf.plot()函数，注意调用的方式跟上一节不同，这里需要指定ax=ax1，volume=ax2，将K线图显示在ax1中，交易量显示在ax2中
        # mpf.plot(self.df,
        #         ax=ax1,
        #         # volume=ax2,
        #         type='candle')
        # # fig.show()		

    def plot(self):
        
        data = pd.DataFrame(index=pd.date_range(end=pd.Timestamp.now(), periods=10, freq='h'))
        data['Open'] = 0
        data['High'] = 0
        data['Low'] = 0
        data['Close'] = 0
        data['Volume'] = 0
        print(data)
        ax1 = self.fig.add_axes([0.2, 0.2 ,0.78, 0.78])
        ax1.set_ylabel('价格')
        mpf.plot(data,
                ax=ax1,
                # volume=ax2,
                type='candle')
        # fig.show()
        
    def plot_data(self, data):
        
        df = pd.DataFrame(data, columns=['datetime', 'Open', 'High', 'Low', 'Close', 'Volume', 'CloseTime', 'QuoteVolume', 'NumberTrades', 'BuyBaseVolume', 'BuyQuoteVolume', 'Ignored'], dtype=float)
        df['datetime'] = pd.to_datetime(df['datetime'] / 1000.0 , unit='s')
        df.set_index('datetime', inplace=True)
        ax1 = self.fig.add_axes([0.2, 0.2 ,0.78, 0.78])
        ax1.set_ylabel('价格')
        mpf.plot(df,
                ax=ax1,
                # volume=ax2,
                type='candle')
        self.draw()