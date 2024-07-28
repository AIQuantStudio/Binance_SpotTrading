from PyQt6.QtCore import *
from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
from functools import partial

from config import ModelConfig
from model import ModelFactory


class SelectModelDialog(QDialog):

    def __init__(self, parent_widget):
        super().__init__(parent_widget)

        self.setWindowTitle("选择模型")
        self.setFixedSize(300, 180)

        layout = QVBoxLayout()
        layout.setSpacing(10)

        label = QLabel("请选择一个模型", self)
        label.setFixedHeight(20)
        layout.addWidget(label)

        for idx, name in enumerate(ModelConfig.Models):
            btn = QPushButton(name, self)
            btn.setFocusPolicy(Qt.FocusPolicy.NoFocus)
            btn.clicked.connect(partial(self.on_click_load_parameters, idx))
            layout.addWidget(btn)

        button_cancel = QPushButton("取  消", self)
        button_cancel.setStyleSheet("QPushButton {margin: 10px 20px 0;}")
        button_cancel.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        button_cancel.clicked.connect(self.reject)
        layout.addWidget(button_cancel)

        self.setLayout(layout)

    def on_click_load_parameters(self, idx):
        cls = list(ModelConfig.Models.values())[idx]["class"]
        id = ModelFactory().create_model(cls)
        if id < 0:
            QMessageBox.warning(self, "警告", f"模型 {list(ModelConfig.Models.keys())[idx]} 加载失败！", QMessageBox.StandardButton.Ok)
            return
        
        filename, _ = QFileDialog.getOpenFileName(self.parentWidget(), "选择参数文件", r".", "参数文件(*.pth)")
        if filename is not None and len(filename) > 0:
            if not ModelFactory().load_data(id, filename):
                ModelFactory().remove_model(id)
                QMessageBox.warning(self, "警告", f"数据加载失败,请检查！", QMessageBox.StandardButton.Ok)
                return

            # 打印模型参数
            # config = ModelFactory().get_config_dict(id)
            # if config is not None:
            #     s = ""
            #     max_len = 0
            #     for key in config.keys():
            #         if len(key) > max_len:
            #             max_len = len(key)
            #     for key, value in config.items():
            #         s = s + f"{key:<{max_len+1}}: {value}\n"

            #     print(s)

            self.done(id)
        else:
            ModelFactory().remove_model(id)
