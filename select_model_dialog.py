from PyQt6.QtWidgets import QApplication, QDialog, QVBoxLayout, QLabel, QPushButton

from config import Config_Data, ModelConfig
from functools import partial


class CustomDialog(QDialog):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("选择模型")
        self.setFixedSize(300, 150)

        layout = QVBoxLayout()

        label = QLabel("请选择一个执行的模型", self)
        layout.addWidget(label)

        for idx, name in enumerate(ModelConfig.Models):
            print(idx)
            print(name)
            btn = QPushButton(name, self)
            btn.clicked.connect(partial(self.done, idx))
            layout.addWidget(btn)

        button_cancel = QPushButton("取消", self)
        button_cancel.clicked.connect(partial(self.done, -1))
        layout.addWidget(button_cancel)

        self.setLayout(layout)
