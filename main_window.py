from PyQt6.QtCore import *
from PyQt6.QtWidgets import *
from PyQt6.QtGui import *

from config import Config
from widget import MainDock, SelectModelDialog, AboutDialog
from model import ModelFactory


class MainWindow(QMainWindow):

    def __init__(self, app_title, app_engine):
        super().__init__()

        self.app_engine = app_engine
        self.dock_widgets = []

        self.setWindowTitle(app_title)
        self.setup_ui()

    def setup_ui(self):
        self.resize(Config.get("main_window.width", 900), Config.get("main_window.height", 600))

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

        self.addToolBar(Qt.ToolBarArea.TopToolBarArea, self.app_toolbar)

    def on_click_select_model(self):
        model_id = SelectModelDialog(self).exec()
        if model_id != QDialog.DialogCode.Rejected:
            model_name = ModelFactory().get_model_name(model_id)
            main_dock = MainDock(self, model_name, model_id, self.app_engine)
            self.addDockWidget(Qt.DockWidgetArea.TopDockWidgetArea, main_dock, Qt.Orientation.Vertical)
            self.dock_widgets.append(main_dock)

    def on_click_about(self):
        dialog = AboutDialog(self, self.app_engine)
        dialog.exec()
        
    def remove_dock_widget(self, dock_widget):
        if dock_widget in self.dock_widgets:
            self.dock_widgets.remove(dock_widget)

    def closeEvent(self, event):
        """重写 QMainWindow::closeEvent"""
        reply = QMessageBox.question(self, "退出", "确认退出？", QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No, QMessageBox.StandardButton.No)
        if reply == QMessageBox.StandardButton.Yes:
            for dock in self.dock_widgets:
                dock.dock_frame.close()
            self.dock_widgets = []
            self.app_engine.close()
            event.accept()
            QApplication.quit()
        else:
            event.ignore()
        # self.app_engine.close()
        # event.accept()
        # QApplication.quit()
