from PyQt6.QtWidgets import QDialog, QVBoxLayout, QLabel, QPushButton
from PyQt6.QtCore import Qt

from config import Accounts
from functools import partial


class SelectAccountDialog(QDialog):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("选择Binance账号")
        self.setFixedSize(300, 150)

        layout = QVBoxLayout()

        label = QLabel("请选择一个可用的账号", self)
        layout.addWidget(label)

        for idx, account in enumerate(Accounts.data):
            print(idx)
            print(account)
            btn = QPushButton(account["Name"], self)
            btn.setFocusPolicy(Qt.FocusPolicy.NoFocus)
            btn.clicked.connect(partial(self.done, idx))
            layout.addWidget(btn)

        button_cancel = QPushButton("取消", self)
        button_cancel.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        button_cancel.clicked.connect(partial(self.done, -1))
        layout.addWidget(button_cancel)

        self.setLayout(layout)
