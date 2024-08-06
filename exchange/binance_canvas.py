import pandas as pd
import numpy as np
import matplotlib
import mplfinance as mpf
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from PyQt6.QtWidgets import *


# plt.rcParams['font.sans-serif'] = ['SimHei']
# plt.rcParams['axes.unicode_minus'] = False
matplotlib.use("QtAgg")
# matplotlib.rcParams["font.sans-serif"] = ["Apple LiSung"]
matplotlib.rcParams["axes.unicode_minus"] = False
STYLE_DICT = {
    "xtick.color": "white", 
    "ytick.color": "white", 
    "xtick.labelcolor": "white", 
    "ytick.labelcolor": "white", 
    "axes.spines.top": False, 
    "axes.spines.right": False, 
    "axes.labelcolor": "white"
    }


class BinanceCanvas(FigureCanvas):

    def __init__(self, width=12, height=8, dpi=100):
        self.predict_price = None
        
        mcolors = mpf.make_marketcolors(up="green", down="red", edge="in", wick="in")
        my_style = mpf.make_mpf_style(base_mpf_style="binance", marketcolors=mcolors, facecolor="#19232D", figcolor="#111111", rc=STYLE_DICT)
        self.fig = mpf.figure(style=my_style, figsize=(width, height), dpi=dpi)
        
        super(BinanceCanvas, self).__init__(self.fig)

        # self.fig.text(0.20, 0.90, '低价: ', fontdict={"color":"white","horizontalalignment":"right","fontname": "Heiti TC"})
        self.fig.text(0.16, 0.90, 'low : ', fontdict={"color":"white","horizontalalignment":"right"})
        self.t1 = self.fig.text(0.16, 0.90, '', fontdict={"color":"white","horizontalalignment":"left"})
        self.fig.text(0.16, 0.95, 'high : ', fontdict={"color":"white","horizontalalignment":"right"})
        self.t2 = self.fig.text(0.16, 0.95, '', fontdict={"color":"white","horizontalalignment":"left"})
        
        self.fig.text(0.45, 0.90, 'volume : ', fontdict={"color":"white", "horizontalalignment":"right"})
        self.t3 = self.fig.text(0.45, 0.90, '', fontdict={"color":"white","horizontalalignment":"left"})
        self.fig.text(0.45, 0.95, 'price : ', fontdict={"color":"white", "horizontalalignment":"right"})
        self.t4 = self.fig.text(0.45, 0.95, '', fontdict={"color":"white","horizontalalignment":"left"})
        
        self.fig.text(0.78, 0.93, 'predict: ', fontdict={"color":"red", "horizontalalignment":"right"})
        self.t5 = self.fig.text(0.78, 0.93, '', fontdict={"color":"white","horizontalalignment":"left"})

        self.ax_kline = self.fig.add_axes([0.08, 0.1, 0.90, 0.78])
        self.ax_kline.set_ylabel('Pri')
        

        
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

    # def plot(self):

        # data = pd.DataFrame(index=pd.date_range(end=pd.Timestamp.now(), periods=10, freq="h"))
        # data["Open"] = 0
        # data["High"] = 0
        # data["Low"] = 0
        # data["Close"] = 0
        # data["Volume"] = 0
        # self.ax1 = self.fig.add_axes([0.2, 0.2 ,0.78, 0.78])

        # mpf.plot(data,
        #         ax=self.ax1,
        #         # volume=ax2,
        #         type='candle')
        # # fig.show()

    def plot_data(self, data):
        df = pd.DataFrame(data, columns=["datetime", "Open", "High", "Low", "Close", "Volume", "CloseTime", "QuoteVolume", "NumberTrades", "BuyBaseVolume", "BuyQuoteVolume", "Ignored"], dtype=float)
        df["datetime"] = pd.to_datetime(df["datetime"] / 1000.0, unit="s")
        df.set_index("datetime", inplace=True)
        
        last_data = df.iloc[-1]
        ap = mpf.make_addplot(df[["Close"]], ax=self.ax_kline)

        self.ax_kline.clear()
        self.ax_kline.set_ylabel("ssss")
        
        self.t1.set_text(f'{last_data["Low"]}')
        self.t2.set_text(f'{last_data["High"]}')
        self.t3.set_text(f'{last_data["Volume"]}')
        self.t4.set_text(f'{last_data["Close"]}')
        
        if self.predict_price is not None:
            self.t5.set_text(f'{self.predict_price:.4f}')

        mpf.plot(
            df,
            ax=self.ax_kline,
            addplot=ap,
            # volume=ax2,
            type="candle",
        )
        self.draw()
        
    def set_predict_price(self, price):
        self.predict_price = price
