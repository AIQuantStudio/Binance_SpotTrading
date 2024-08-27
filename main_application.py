from PyQt6.QtGui import *
from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from main_engine import MainEngine
import sys
import traceback
import types
import qdarkstyle
import platform
import ctypes

from config import Config


def create_application(app_name):
    sys.excepthook = excepthook
    
    Config.init_config()
    MainEngine.start()

    app = QApplication(sys.argv)
    app.setQuitOnLastWindowClosed(True)
    app.setStyleSheet(qdarkstyle.load_stylesheet_pyqt6())
    app.setFont(QFont(Config.get("font.family"), Config.get("font.size")))
    app.setWindowIcon(QIcon(("logo.ico")))
    app.setApplicationDisplayName(app_name)
    if "Windows" in platform.uname():
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(app_name)
    return app


def excepthook(exctype: type, value: Exception, tb: types.TracebackType) -> None:
    """自定义全局异常钩子，由对话框展示异常信息"""

    class ExceptionDialog(QDialog):
        def __init__(self, msg: str):
            super().__init__()
            self.msg: str = msg
            self.init_ui()

        def init_ui(self) -> None:
            self.setWindowTitle("触发异常")
            self.setFixedSize(400, 300)

            self.msg_edit = QTextEdit()
            self.msg_edit.setText(self.msg)
            self.msg_edit.setReadOnly(True)

            copy_button = QPushButton("复制")
            copy_button.clicked.connect(self.doCopyText)

            close_button = QPushButton("关闭")
            close_button.clicked.connect(self.close)

            destory_button = QPushButton("退出")
            destory_button.clicked.connect(self.doDestory)

            hbox = QHBoxLayout()
            hbox.addWidget(copy_button)
            hbox.addWidget(close_button)
            hbox.addWidget(destory_button)

            vbox = QVBoxLayout()
            vbox.addWidget(self.msg_edit)
            vbox.addLayout(hbox)

            self.setLayout(vbox)

        def doCopyText(self) -> None:
            self.msg_edit.selectAll()
            self.msg_edit.copy()

        def doDestory(self) -> None:
            ret = QMessageBox.question(self, "确认", "是否确定退出程序？", QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
            if ret == QMessageBox.StandardButton.Yes:
                QApplication.exit(0)

    sys.__excepthook__(exctype, value, tb)

    msg = "".join(traceback.format_exception(exctype, value, tb))
    dialog = ExceptionDialog(msg)
    dialog.exec()
