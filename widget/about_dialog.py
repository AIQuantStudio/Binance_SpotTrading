from PyQt6.QtCore import *
from PyQt6.QtWidgets import *
from PyQt6.QtGui import *

import requests
import platform
import numpy as np

from config import _Version


class AboutDialog(QDialog):

    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self) -> None:
        self.setWindowTitle(f"关于")
        
        text = f"""
            Spot Trading (Binance) {_Version}
            
                 Python - {platform.python_version()}
                 PyQt6 - {PYQT_VERSION_STR}
                 Numpy - {np.__version__}
            
            {requests.get('https://myip.ipip.net', timeout=5).text}
            """

        content_label = QLabel()
        content_label.setText(text)
        content_label.setTextInteractionFlags(Qt.TextInteractionFlag.TextSelectableByMouse)
        content_label.setMinimumWidth(500)

        vbox_layout = QVBoxLayout()
        vbox_layout.addWidget(content_label)
        vbox_layout.setSizeConstraint(QLayout.SizeConstraint.SetFixedSize)
        self.setLayout(vbox_layout)
        

