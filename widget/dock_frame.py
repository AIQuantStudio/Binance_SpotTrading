from PyQt6.QtCore import *
from PyQt6.QtWidgets import *
from PyQt6.QtGui import *

from widget.model_panel import ModelPanel
from widget.trade_panel import TradePanel


class DockFrame(QFrame):

    def __init__(self, top_dock):
        super().__init__(top_dock)

        self.top_dock = top_dock

        self.setLineWidth(1)
        self.setMidLineWidth(1)
        self.setFrameStyle(QFrame.Shape.Box | QFrame.Shadow.Sunken)

        vbox_layout = QVBoxLayout()
        vbox_layout.setContentsMargins(5, 0, 0, 0)
        self.setLayout(vbox_layout)

        self.model_panel = ModelPanel(self, self.top_dock)
        vbox_layout.addWidget(self.model_panel, stretch=6)

        self.line = QFrame(self)
        self.line.setGeometry(QRect(0, 120, 341, 20))
        self.line.setFrameShadow(QFrame.Shadow.Sunken)
        self.line.setLineWidth(5)
        self.line.setFrameShape(QFrame.Shape.HLine)
        vbox_layout.addWidget(self.line)

        self.trade_panel = TradePanel(self, self.top_dock)
        vbox_layout.addWidget(self.trade_panel, stretch=4)

    def close(self)->bool:
        self.model_panel.close()
        self.trade_panel.close()
        return super().close()
