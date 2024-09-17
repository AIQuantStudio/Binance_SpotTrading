from PyQt6.QtCore import *
from PyQt6.QtWidgets import *
from PyQt6.QtGui import *

from common.enumeration import Trend

COLOR_RISE = QColor("red")
COLOR_FALL = QColor("green")


class PredictPriceTrendCell(QTableWidgetItem):
    """"""

    def __init__(self, content: Trend):
        """"""
        super().__init__()

        self.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
        self.set_content(content)

    def set_content(self, content: Trend) -> None:
        """"""
        if content is Trend.RISE:
            self.setData(Qt.ItemDataRole.ForegroundRole, QBrush(COLOR_RISE))
            # self.setForeground(COLOR_SELL)
        else:
            # self.setForeground(COLOR_BUY)
            self.setData(Qt.ItemDataRole.ForegroundRole, QBrush(COLOR_FALL))

        self.setText(str(content.value))