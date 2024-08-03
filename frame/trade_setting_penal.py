from PyQt6.QtCore import *
from PyQt6.QtWidgets import *
from PyQt6.QtGui import *


class TradeSettingPenal(QFrame):

    def __init__(self, parent_widget, top_dock, app_engine):
        super().__init__(parent_widget)

        self.top_dock = top_dock
        self.app_engine = app_engine

        self.setup_ui()

    def setup_ui(self):
        vbox_layout = QVBoxLayout()
        self.setLayout(vbox_layout)

        self.table = QTableWidget(4,3,self)
        self.table.setHorizontalHeaderLabels(['第一列', '第二列', '第三列'])

        vbox_layout.addWidget(self.table)
