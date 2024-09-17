from PyQt6.QtCore import *
from PyQt6.QtWidgets import *
from PyQt6.QtGui import *

from common.enumeration import Direction

COLOR_BUY = QColor("red")
COLOR_SELL = QColor("green")


class TradeHistoryDirectionCell(QTableWidgetItem):
    """"""

    def __init__(self, content: Direction):
        """"""
        super().__init__()

        self.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
        self.set_content(content)

    def set_content(self, content: Direction) -> None:
        """"""
        if content is Direction.SELL:
            self.setForeground(COLOR_SELL)
        else:
            self.setForeground(COLOR_BUY)

        self.setText(str(content.value))