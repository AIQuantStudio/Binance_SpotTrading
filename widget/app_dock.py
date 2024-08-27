from PyQt6.QtCore import *
from PyQt6.QtWidgets import *
from PyQt6.QtGui import *

# from app_engine import MainEngine
# from model import ModelFactory

from widget.app_win import AppWin


class AppDock(QDockWidget):

    def __init__(self, parent_widget, name, id):
        super().__init__(name, parent_widget)

        self.app_id = id
        self.app_win = AppWin(self, self.app_id)
        
        self.setObjectName(str(self.app_id))
        self.setFeatures(QDockWidget.DockWidgetFeature.DockWidgetClosable | QDockWidget.DockWidgetFeature.DockWidgetFloatable | QDockWidget.DockWidgetFeature.DockWidgetMovable)
        self.setAllowedAreas(Qt.DockWidgetArea.TopDockWidgetArea | Qt.DockWidgetArea.BottomDockWidgetArea)
        self.setWidget(self.app_win)

    def register_close_signal(self, signal: pyqtSignal):
        self.close_signal = signal

    def closeEvent(self, event: QCloseEvent) -> None:
        """ 重写 AppDock::closeEvent """
        reply = QMessageBox.question(self, "关闭", "确认关闭？", QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No, QMessageBox.StandardButton.No)
        if reply == QMessageBox.StandardButton.Yes:
            self.app_win.close()
            self.close_signal.emit(self)
            event.accept()
        else:
            event.ignore()

    def close(self) -> bool:
        return self.app_win.close()
