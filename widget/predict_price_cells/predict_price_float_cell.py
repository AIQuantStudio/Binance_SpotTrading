from PyQt6.QtCore import *
from PyQt6.QtWidgets import *
from PyQt6.QtGui import *


class PredictPriceFloatCell(QTableWidgetItem):
    """"""

    def __init__(self, content: float):
        """"""
        super().__init__()
        self.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
        self.set_content(content)

    def set_content(self, content: float, precision=6) -> None:
        """"""
        self.setText(format(content, f".{precision}f"))
