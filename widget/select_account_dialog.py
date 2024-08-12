from PyQt6.QtCore import *
from PyQt6.QtWidgets import *
from PyQt6.QtGui import *

# from config import Accounts
from functools import partial

from account import AccountFactory
from structure import BianceAccountData, BianceTestAccountData
from setting import AccountSetting


class SelectAccountDialog(QDialog):
    def __init__(self, parent_widget, model_id):
        super().__init__(parent_widget)
        
        self.model_id = model_id
        self.setWindowTitle("选择Binance账号")
        self.setFixedSize(300, 120 + 30*len(AccountSetting.Accounts))

        layout = QVBoxLayout()
        layout.setSpacing(10)

        label = QLabel("请选择一个可用的账号", self)
        label.setFixedHeight(20)
        layout.addWidget(label)

        for idx, account in enumerate(AccountSetting.Accounts):
            # if account["Name"].startswith("[TEST]"):
            #     btn = QPushButton(account["Name"], self)
            #     btn.setFocusPolicy(Qt.FocusPolicy.NoFocus)
            #     btn.clicked.connect(partial(self.on_click_load_test_account, account))
            #     layout.addWidget(btn)
            # else:
            #     btn = QPushButton(account["Name"], self)
            #     btn.setFocusPolicy(Qt.FocusPolicy.NoFocus)
            #     btn.clicked.connect(partial(self.on_click_load_binance_account, account))
            #     layout.addWidget(btn)
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

    # def on_click_load_binance_account(self, data):
    #     ba = BianceAccountData(name=data["Name"], id=data["Account"], api_key=data["ApiKey"], secret_key=data["SecertKey"])

    #     success = BinanceFactory().load_account(self.model_id, ba)
    #     if not success:
    #         QMessageBox.warning(self, "警告", f"Binance账户[{data['Name']}]加载失败！", QMessageBox.StandardButton.Ok)
    #         return

    #     self.accept()
    
    # def on_click_load_test_account(self, data):
    #     ba = BianceTestAccountData(name=data["Name"], id=data["Account"], db=data["DB"])

    #     success = BinanceTestFactory().load_account(self.model_id, ba)
    #     if not success:
    #         QMessageBox.warning(self, "警告", f"测试账户[{data['Name']}]加载失败！", QMessageBox.StandardButton.Ok)
    #         return

    #     self.accept()
        
    def on_click_load_account(self, account_data):
        # ba = BianceTestAccountData(name=data["Name"], id=data["Account"], db=data["DB"])

        success = AccountFactory().load_account(self.model_id, account_data)
        if not success:
            QMessageBox.warning(self, "警告", f"账户[{account_data['Name']}]加载失败！", QMessageBox.StandardButton.Ok)
            return

        self.accept()