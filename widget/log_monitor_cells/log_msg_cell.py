from PyQt6.QtCore import *
from PyQt6.QtWidgets import *
from PyQt6.QtGui import *


class LogMsgCell(QTableWidgetItem):

    def __init__(self, content: str):
        super().__init__()
        self.setTextAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
        self.set_content(content)

    def set_content(self, content: str):
        self.setText(content)
