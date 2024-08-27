from PyQt6.QtCore import *
from PyQt6.QtWidgets import *
from PyQt6.QtGui import *

from main_engine import MainEngine
from config import Config
from widget import AppDock, SelectModelDialog, AboutDialog
from model import ModelFactory


class MainWindow(QMainWindow):

    signal_close_app: pyqtSignal = pyqtSignal(AppDock)

    def __init__(self, app_title):
        super().__init__()

        self.app_docks: list[AppDock] = list()

        self.setWindowTitle(app_title)
        self.setup_ui()

        self.signal_close_app.connect(self.process_close_app)

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
            model_symbol = ModelFactory().get_model_symbol(model_id)
            app_dock = AppDock(self, f"{model_name} {model_symbol}", model_id)
            app_dock.register_close_signal(self.signal_close_app)
            self.addDockWidget(Qt.DockWidgetArea.TopDockWidgetArea, app_dock, Qt.Orientation.Vertical)
            self.app_docks.append(app_dock)

    def on_click_about(self):
        dlg = AboutDialog(self)
        dlg.exec()

    def process_close_app(self, app: AppDock):
        if app in self.app_docks:
            self.app_docks.remove(app)

    def closeEvent(self, event: QEvent) -> None:
        """ 重写 QMainWindow::closeEvent """
        reply = QMessageBox.question(self, "退出", "确认退出？", QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No, QMessageBox.StandardButton.No)
        if reply == QMessageBox.StandardButton.Yes:
            for app in self.app_docks:
                app.close()
            self.app_docks = []
            MainEngine.close()
            event.accept()
            QApplication.quit()
        else:
            event.ignore()
