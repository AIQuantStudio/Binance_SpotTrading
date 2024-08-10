from PyQt6.QtCore import *
from PyQt6.QtWidgets import *
from PyQt6.QtGui import *

from widget.dock_frame import DockFrame


class MainDock(QDockWidget):
    
    def __init__(self, parent_widget, name, id, app_engine):
        super().__init__(name, parent_widget)
        
        self.id = id
        self.app_engine = app_engine
        
        self.dock_frame = DockFrame(self, app_engine)
        self.setObjectName(str(self.id))
        self.setFeatures(QDockWidget.DockWidgetFeature.DockWidgetClosable | QDockWidget.DockWidgetFeature.DockWidgetFloatable | QDockWidget.DockWidgetFeature.DockWidgetMovable)
        self.setAllowedAreas(Qt.DockWidgetArea.TopDockWidgetArea | Qt.DockWidgetArea.BottomDockWidgetArea)
        self.setWidget(self.dock_frame)
        self.windowTitle()
        
    def closeEvent(self, event):
        """重写 MainDock::closeEvent"""
        print(11111111111111111111111111111)
        print(event)
        reply = QMessageBox.question(self, "关闭", "确认关闭？", QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No, QMessageBox.StandardButton.No)
        if reply == QMessageBox.StandardButton.Yes:
            self.dock_frame.close()
            self.parentWidget().remove_dock_widget(self)
            event.accept()
        else:
            event.ignore()
        
        
        
        
