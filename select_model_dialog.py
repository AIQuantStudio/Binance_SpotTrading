from PyQt6.QtCore import *
from PyQt6.QtWidgets import *
from PyQt6.QtGui import *

from config import Config_Data, ModelConfig
from model import ModelFactory
from functools import partial


class SelectModelDialog(QDialog):
    def __init__(self, parent_widget):
        super().__init__(parent_widget)

        self.setWindowTitle("选择模型")
        self.setFixedSize(300, 150)

        layout = QVBoxLayout()

        label = QLabel("请选择一个模型", self)
        layout.addWidget(label)

        for idx, name in enumerate(ModelConfig.Models):
            btn = QPushButton(name, self)
            btn.setFocusPolicy(Qt.FocusPolicy.NoFocus)
            btn.clicked.connect(partial(self.on_click_load_parameters, idx))
            layout.addWidget(btn)

        button_cancel = QPushButton("取消", self)
        button_cancel.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        button_cancel.clicked.connect(self.reject)
        layout.addWidget(button_cancel)

        self.setLayout(layout)

    def on_click_load_parameters(self, idx):
        cls = list(ModelConfig.Models.values())[idx]["class"]
        id = ModelFactory.create_model(cls)
        filename, _ = QFileDialog.getOpenFileName(self.parentWidget(), "选择参数文件", r".", "参数文件(*.pth)")
        if filename is not None and len(filename) > 0:
            ModelFactory.load_data(id, filename)
            config = ModelFactory.get_config_dict(id)
            if config is not None:
                s = ""
                max_len = 0
                for key in config.keys():
                    if len(key) > max_len:
                        max_len = len(key)
                for key, value in config.items():
                    s = s + f"{key:<{max_len+1}}: {value}\n"
                    
                # self.config_info_textbrowser.setText(s)
                print(s)
            self.done(id)
        else:
            ModelFactory.remove_model(id)
        
                