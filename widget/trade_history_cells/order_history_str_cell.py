from PyQt6.QtCore import *
from PyQt6.QtWidgets import *
from PyQt6.QtGui import *


class OrderHistoryStrCell(QTableWidgetItem):
    """"""

    def __init__(self, content: str):
        """"""
        super().__init__()

        self.content = content
        self.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
        self.set_content(content)

    def set_content(self, content: str) -> None:
        """"""
        self.content = content
        self.setText(content)

    def __hash__(self):
        return hash(id(self.content))

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return hash(id(self.content)) == hash(id(other.content))
        else:
            return False
