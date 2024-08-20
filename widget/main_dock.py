from PyQt6.QtCore import *
from PyQt6.QtWidgets import *
from PyQt6.QtGui import *

# from app_engine import AppEngine
# from model import ModelFactory

from widget.dock_frame import DockFrame


class MainDock(QDockWidget):

    def __init__(self, parent_widget, name, id):
        super().__init__(name, parent_widget)

        self.id = id

        self.dock_frame = DockFrame(self)
        self.setObjectName(str(self.id))
        self.setFeatures(QDockWidget.DockWidgetFeature.DockWidgetClosable | QDockWidget.DockWidgetFeature.DockWidgetFloatable | QDockWidget.DockWidgetFeature.DockWidgetMovable)
        self.setAllowedAreas(Qt.DockWidgetArea.TopDockWidgetArea | Qt.DockWidgetArea.BottomDockWidgetArea)
        self.setWidget(self.dock_frame)

    def register_close_signal(self, signal: pyqtSignal):
        self.close_signal = signal

    def closeEvent(self, event: QCloseEvent) -> None:
        """重写 MainDock::closeEvent"""
        reply = QMessageBox.question(self, "关闭", "确认关闭？", QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No, QMessageBox.StandardButton.No)
        if reply == QMessageBox.StandardButton.Yes:
            self.dock_frame.close()
            # self.parentWidget().remove_dock_widget(self)
            self.close_signal.emit(self)
            event.accept()
        else:
            event.ignore()

    def close(self) -> bool:
        return self.dock_frame.close()
