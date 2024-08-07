from PyQt6.QtCore import *
from PyQt6.QtWidgets import *
from PyQt6.QtGui import *

from select_model_dialog import SelectModelDialog
from model.model_factory import ModelFactory
from main_dock import MainDock
from widget import AboutDialog


class MainWindow(QMainWindow):

    def __init__(self, app_title, app_engine):
        super().__init__()

        self.app_engine = app_engine

        self.setWindowTitle(app_title)
        self.setup_ui()

    def setup_ui(self):
        self.resize(1600, 900)

        # 窗体的位置
        fg = self.frameGeometry()
        fg.moveCenter(QApplication.primaryScreen().availableGeometry().center())
        self.move(fg.topLeft())

        self.app_toolbar = QToolBar(self)
        self.app_toolbar.setFloatable(False)
        self.app_toolbar.setMovable(False)
        self.app_toolbar.setIconSize(QSize(26, 26))
        self.app_toolbar.layout().setSpacing(4)

        left_space = QWidget()
        left_space.setFixedWidth(6)
        left_space.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.app_toolbar.addWidget(left_space)

        load_model_action = QAction(QIcon(QPixmap("./ico/load_model.ico")), "加载模型", self)
        load_model_action.triggered.connect(self.on_click_select_model)
        self.app_toolbar.addAction(load_model_action)
        self.app_toolbar.addSeparator()
        
        about_action = QAction(QIcon(QPixmap("./ico/about.ico")), "加载模型", self)
        about_action.triggered.connect(self.on_click_about)
        self.app_toolbar.addAction(about_action)
        # self.app_toolbar.addSeparator()

        self.addToolBar(Qt.ToolBarArea.TopToolBarArea, self.app_toolbar)

    def on_click_select_model(self):
        id = SelectModelDialog(self).exec()
        if id == QDialog.DialogCode.Rejected:
            return
        else:
            self.create_model_panel(id)
    
    def on_click_about(self):
        dialog = AboutDialog()
        dialog.exec()

    def create_model_panel(self, model_id):
        name = ModelFactory().get_model_name(model_id)
        model_dock = MainDock(name, model_id, self.app_engine)
        self.addDockWidget(Qt.DockWidgetArea.TopDockWidgetArea, model_dock, Qt.Orientation.Vertical)

    def closeEvent(self, event):
        """重写 QMainWindow::closeEvent"""
        reply = QMessageBox.question(self, "退出", "确认退出？", QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No, QMessageBox.StandardButton.No)
        if reply == QMessageBox.StandardButton.Yes:
            self.app_engine.close()
            event.accept()
            QApplication.quit()
        else:
            event.ignore()
        # self.app_engine.close()
        # event.accept()
        # QApplication.quit()
