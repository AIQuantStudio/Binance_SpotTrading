from PyQt6.QtCore import *
from PyQt6.QtWidgets import *
from PyQt6.QtGui import *

import requests
import platform
import numpy as np

from main_engine import MainEngine
from config import Version


class AboutDialog(QDialog):

    def __init__(self, parent_widget):
        super().__init__(parent_widget)

        self.init_ui()
        self.bind_event()

    def init_ui(self):
        self.setWindowTitle("关于")

        text = f"""
            Spot Trading (Binance) {Version}
            
                 Python - {platform.python_version()}
                 PyQt6 - {PYQT_VERSION_STR}
                 Numpy - {np.__version__}

            """

        content_label = QLabel()
        content_label.setText(text)
        content_label.setMinimumWidth(360)

        self.ip_label = QLabel()
        self.ip_label.setContentsMargins(10, 0, 0, 0)
        self.ip_label.setText("-")
        self.ip_label.setTextInteractionFlags(Qt.TextInteractionFlag.TextSelectableByMouse)

        vbox_layout = QVBoxLayout()
        vbox_layout.addWidget(content_label)
        vbox_layout.addWidget(self.ip_label)
        vbox_layout.setSizeConstraint(QLayout.SizeConstraint.SetFixedSize)
        self.setLayout(vbox_layout)

    def bind_event(self):
        MainEngine.event_engine.run_async(self.request_ip)

    def request_ip(self):
        try:
            response = requests.get("https://myip.ipip.net", timeout=5)
            if response.status_code == 200:
                self.ip_label.setText(response.text)
        except:
            return
