from PyQt6.QtCore import *
from PyQt6.QtWidgets import *
from PyQt6.QtGui import *

from main_frame import MainFrame


class MainDock(QDockWidget):
    
    def __init__(self, name, id, app_engine):
        super().__init__(name)
        
        self.name = name
        self.id = id
        self.app_engine = app_engine
        
        self.main_frame = MainFrame(self, app_engine)
        self.setObjectName(str(self.id))
        self.setFeatures(QDockWidget.DockWidgetFeature.DockWidgetClosable | QDockWidget.DockWidgetFeature.DockWidgetFloatable | QDockWidget.DockWidgetFeature.DockWidgetMovable)
        self.setAllowedAreas(Qt.DockWidgetArea.TopDockWidgetArea | Qt.DockWidgetArea.BottomDockWidgetArea)
        self.setWidget(self.main_frame)
        self.windowTitle()
        
    def closeEvent(self, event):
        """重写 QMainWindow::closeEvent"""
        reply = QMessageBox.question(self, "关闭", "确认关闭？", QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No, QMessageBox.StandardButton.No)
        if reply == QMessageBox.StandardButton.Yes:
            event.accept()
        else:
            event.ignore()
        
        
        
        
