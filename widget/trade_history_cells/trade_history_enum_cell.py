from PyQt6.QtCore import *
from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
from enum import Enum

class TradeHistoryEnumCell(QTableWidgetItem):
    """"""

    def __init__(self, content: Enum):
        """"""
        super().__init__()
        self.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
        self.set_content(content)

    def set_content(self, content: Enum) -> None:
        """"""
        self.setText(str(content.value))
