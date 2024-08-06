from PyQt6.QtCore import *
from PyQt6.QtWidgets import *
from PyQt6.QtGui import *

from config import Accounts
from functools import partial

from exchange import BinanceFactory
from structure import BianceAccountData
from config import Config_Data


class SelectAccountDialog(QDialog):
    def __init__(self, parent_widget, model_id):
        super().__init__(parent_widget)
        
        self.model_id = model_id
        self.setWindowTitle("选择Binance账号")
        self.setFixedSize(300, 120 + 30*len(Accounts.data))

        layout = QVBoxLayout()
        layout.setSpacing(10)

        label = QLabel("请选择一个可用的账号", self)
        label.setFixedHeight(20)
        layout.addWidget(label)

        for idx, account in enumerate(Accounts.data):
            btn = QPushButton(account["Name"], self)
            btn.setFocusPolicy(Qt.FocusPolicy.NoFocus)
            btn.clicked.connect(partial(self.on_click_load_account, account))
            layout.addWidget(btn)

        button_cancel = QPushButton("取  消", self)
        button_cancel.setStyleSheet("QPushButton {margin: 10px 20px 0;}")
        button_cancel.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        button_cancel.clicked.connect(self.reject)
        layout.addWidget(button_cancel)

        self.setLayout(layout)

    def on_click_load_account(self, data):
        ba = BianceAccountData(name=data["Name"], id=data["Account"], api_key=data["ApiKey"], secret_key=data["SecertKey"])

        success = BinanceFactory().load_account(self.model_id, ba)
        if not success:
            QMessageBox.warning(self, "警告", f"Binance账户[{data['Name']}]加载失败！", QMessageBox.StandardButton.Ok)
            return

        self.accept()
        
            