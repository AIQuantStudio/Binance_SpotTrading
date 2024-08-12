from PyQt6.QtCore import *
from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
from typing import Any
from tzlocal import get_localzone


class PrdictPriceTimeCell(QTableWidgetItem):
    """"""
    local_tz = get_localzone()

    def __init__(self, content: Any):
        """"""
        super().__init__()
        self.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
        self.set_content(content)

    def set_content(self, content: Any) -> None:
        """"""
        if content is None:
            return

        content = content.astimezone(self.local_tz)
        timestamp = content.strftime("%H:%M")
        self.setText(timestamp)
