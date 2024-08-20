from PyQt6.QtCore import *
from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
from datetime import datetime


class LogTimeCell(QTableWidgetItem):
    
    def __init__(self, content: datetime):
        super().__init__()
        self.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
        self.set_content(content)

    def set_content(self, content: datetime):
        if content is None:
            return

        timestamp = content.strftime("%H:%M:%S")
        self.setText(timestamp)
