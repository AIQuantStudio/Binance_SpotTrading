from PyQt6.QtCore import *
from PyQt6.QtWidgets import *
from PyQt6.QtGui import *

from widget import ModelPanel
from widget import TradePanel


class MainFrame(QFrame):

    def __init__(self, top_dock, app_engine):
        super().__init__(top_dock)

        self.top_dock = top_dock
        self.app_engine = app_engine

        self.setLineWidth(1)
        self.setMidLineWidth(1)
        self.setFrameStyle(QFrame.Shape.Box | QFrame.Shadow.Sunken)
        # self.setStyleSheet("QFrame { background-color: blue;}")
        self.setup_ui()
        

    def setup_ui(self):
        vbox_layout = QVBoxLayout()
        vbox_layout.setContentsMargins(5,0,0,0)
        self.setLayout(vbox_layout)

        self.model_penal = ModelPanel(self, self.top_dock, self.app_engine)
        vbox_layout.addWidget(self.model_penal, stretch=6)

        self.line = QFrame(self)
        self.line.setGeometry(QRect(0, 120, 341, 20))
        self.line.setFrameShadow(QFrame.Shadow.Sunken)
        self.line.setLineWidth(5)
        self.line.setFrameShape(QFrame.Shape.HLine)
        vbox_layout.addWidget(self.line)

        self.trade_penal = TradePanel(self, self.top_dock, self.app_engine)
        vbox_layout.addWidget(self.trade_penal, stretch=4)

    def close(self):
        self.model_penal.close()
        self.trade_penal.close()
        return super().close()
