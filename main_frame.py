from PyQt6.QtCore import *
from PyQt6.QtWidgets import *
from PyQt6.QtGui import *

from model_penal import ModelPanel
from trade_penal import TradePanel


class MainFrame(QFrame):

    def __init__(self, top_dock, app_engine):
        super().__init__(top_dock)

        self.top_dock = top_dock
        self.app_engine = app_engine

        self.setLineWidth(1)
        self.setMidLineWidth(1)
        self.setFrameStyle(QFrame.Shape.Box | QFrame.Shadow.Sunken)
        self.setup_ui()

    def setup_ui(self):
        vbox_layout = QVBoxLayout()
        self.setLayout(vbox_layout)

        self.model_penal_widget = ModelPanel(self, self.top_dock, self.app_engine)
        vbox_layout.addWidget(self.model_penal_widget, stretch=6)
        # penal_widget.setFixedHeight(100)
        # penal_widget.setFixedWidth(100)
        # penal_widget.setStyleSheet("background-color: blue;")

        self.line = QFrame(self)
        self.line.setGeometry(QRect(0, 120, 341, 20))
        self.line.setFrameShadow(QFrame.Shadow.Sunken)
        self.line.setLineWidth(5)
        self.line.setFrameShape(QFrame.Shape.HLine)
        vbox_layout.addWidget(self.line)

        trade_penal_widget = TradePanel(self, self.top_dock, self.app_engine)
        vbox_layout.addWidget(trade_penal_widget, stretch=4)

    def close(self):
        self.model_penal_widget.close()
        return super().close()