import mplfinance as mpf
import pandas as pd
import matplotlib as mpl
mpl.use('QtAgg')
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from PyQt6.QtWidgets import *
import sys
from matplotlib.animation import FuncAnimation


class MyFigure(FigureCanvas):
    def __init__(self, width=12, height=8, dpi=100):
        mcolors = mpf.make_marketcolors(up='red',
                                        down='green',
                                        edge='in',
                                        wick='in',
                                        volume='in')
        my_style = mpf.make_mpf_style(base_mpf_style='binance',
                                      marketcolors=mcolors,
                                      facecolor='black',
                                      mavcolors=['blue', 'red', 'yellow'])

        self.fig=mpf.figure(style=my_style, figsize=(width,height), dpi=dpi)
        super(MyFigure,self).__init__(self.fig)
        self.df = pd.read_csv('./data/SPY_20110701_20120630_Bollinger.csv', index_col=0, parse_dates=True)
        self.fig.subplots_adjust(left=0, bottom=0, right=1, top=0.95, hspace=0)
        self.ax1, self.ax2 = self.fig.subplots(nrows=2, ncols=1, sharex=True)
        mpf.plot(self.df.head(50), ax=self.ax1, type='candle', volume=self.ax2, mav=[5, 10, 30], axtitle='customize plot', tight_layout=True)

class MyWin(QWidget):
    def __init__(self):
        super().__init__()
        self.myfig=MyFigure()
        self.setWindowTitle('plot candle figure')

        self.btn1 = QPushButton('start')
        self.btn1.clicked.connect(self.on_start)
        self.btn2 = QPushButton('stop')
        self.btn2.clicked.connect(self.on_stop)
        hbox = QHBoxLayout()
        hbox.addWidget(self.btn1)
        hbox.addWidget(self.btn2)

        layout=QVBoxLayout()
        layout.addWidget(self.myfig)
        layout.addLayout(hbox)
        self.setLayout(layout)

    def on_start(self):
        self.ani = FuncAnimation(self.myfig.fig, self.update_candle, frames=100, interval=100)

    def on_stop(self):
        self.ani._stop()

    def update_candle(self, steps):
        end = 50 + steps
        self.myfig.fig.clear()
        self.myfig.ax1, self.myfig.ax2 = self.myfig.fig.subplots(nrows=2, ncols=1, sharex=True)
        mpf.plot(self.myfig.df.iloc[0:end], ax=self.myfig.ax1, type='candle', volume=self.myfig.ax2,
                 mav=[5, 10, 30], axtitle='customize plot', tight_layout=True)


if __name__=='__main__':
    app=QApplication(sys.argv)
    winform=MyWin()
    winform.show()
    sys.exit(app.exec())
