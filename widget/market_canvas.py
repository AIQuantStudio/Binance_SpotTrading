from PyQt6.QtCore import *
from PyQt6.QtWidgets import *
from PyQt6.QtGui import *

from widget.market_figure import MarketFigure


class MarketCanvas(QFrame):

    def __init__(self, parent_widget, top_dock, app_engine):
        super().__init__(parent_widget)
        
        self.top_dock = top_dock
        self.app_engine = app_engine

        self.setLineWidth(1)
        self.setMidLineWidth(1)
        self.setFrameStyle(QFrame.Shape.Panel | QFrame.Shadow.Raised)
        self.setStyleSheet("background-color:#2a2a2a")
        
        
        hbox_layout = QHBoxLayout()
        last_high_label = QLabel("最高价")
        
        self.last_high = QLabel("")
        self.last_low = QLabel("")
        self.last_close = QLabel("")
        self.last_volume = QLabel("")
        
        vbox_layout = QVBoxLayout(self)
        grid = QGridLayout()
        grid.addWidget(, 0, 0)
        grid.addWidget(QLabel("最低价"), 1, 0)
        grid.addWidget(QLabel("成交价"), 0, 1)
        grid.addWidget(QLabel("交易量"), 1, 1)
        # grid.addWidget(self.last_high, 0, 0, 1, 2)
        # grid.addWidget(self.last_low, 1, 0, 1, 2)
        # grid.addWidget(self.last_close, 0, 1, 1, 2)
        # grid.addWidget(self.last_volume, 1, 1, 1, 2)

        vbox_layout.addLayout(grid)

        self.market_figure = MarketFigure()
        vbox_layout.addWidget(self.market_figure)
        
        self.setLayout(vbox_layout)

    
      