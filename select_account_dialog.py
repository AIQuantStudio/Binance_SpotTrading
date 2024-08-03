from PyQt6.QtCore import *
from PyQt6.QtWidgets import *
from PyQt6.QtGui import *

from config import Accounts
from functools import partial

from exchange import BinanceFactory
from structure import BianceAccountData


class SelectAccountDialog(QDialog):
    def __init__(self, parent_widget, model_id):
        super().__init__(parent_widget)
        
        self.model_id = model_id
        self.setWindowTitle("选择Binance账号")
        self.setFixedSize(300, 150)

        layout = QVBoxLayout()
        layout.setSpacing(10)

        label = QLabel("请选择一个可用的账号", self)
        label.setFixedHeight(20)
        layout.addWidget(label)

        for idx, account in enumerate(Accounts.data):
            print(idx)
            print(account)
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
            QMessageBox.warning(self, "警告", f"Binance账户[{data["Name"]}]加载失败！", QMessageBox.StandardButton.Ok)
            return

        filename, _ = QFileDialog.getOpenFileName(self.parentWidget(), "选择参数文件", Config_Data["model.path"], "参数文件(*.pth)")
        if filename is not None and len(filename) > 0:
            if not ModelFactory().load_data(id, filename):
                ModelFactory().remove_model(id)
                QMessageBox.warning(self, "警告", f"数据加载失败,请检查！", QMessageBox.StandardButton.Ok)
                return
            self.done(id)
        else:
            ModelFactory().remove_model(id)