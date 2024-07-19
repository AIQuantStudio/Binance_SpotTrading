from PyQt6.QtWidgets import QApplication, QDialog, QVBoxLayout, QLabel, QPushButton


class CustomDialog(QDialog):
    def __init__(self):
        super().__init__()

        self.setWindowTitle('选择模型')
        self.setFixedSize(300, 150)

        layout = QVBoxLayout()

        label = QLabel('请选择一个执行的模型', self)
        layout.addWidget(label)

        button_ok = QPushButton('确定', self)
        button_ok.clicked.connect(self.accept)
        layout.addWidget(button_ok)

        button_cancel = QPushButton('取消', self)
        button_cancel.clicked.connect(self.reject)
        layout.addWidget(button_cancel)

        self.setLayout(layout)