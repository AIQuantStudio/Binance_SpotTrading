from PyQt6.QtCore import *
from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
from PyQt6.QtWebEngineWidgets import QWebEngineView
from PyQt6.QtWebEngineCore import QWebEngineProfile, QWebEngineUrlScheme

import asyncio

# from views.bbin_webengine_view import BBINWebEngineView
# from core.bbin_request_interceptor import BBINRequestInterceptor
# from core.bbin_webengine_page import BBINWebEnginePage
# from core.bbin_ws_scheme_handler import BBINWebsocketSchemeHandler
# from views.adminWebEngine import AdminWebEngine
from config import Config_Data, ModelConfig
from config import Accounts
from select_model_dialog import SelectModelDialog
from select_account_dialog import SelectAccountDialog
from model.model_factory import ModelFactory
from binance_account import BinanceAccount
from main_dock import MainDock


class MainWindow(QMainWindow):

    def __init__(self, app_title, app_engine):
        super().__init__()

        self.app_engine = app_engine

        self.setWindowTitle(app_title)
        self.setup_ui()
        # self.bind_event()

        # self.init_default_status()

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

        action = QAction(QIcon(QPixmap("./ico/load_model.ico")), "加载模型", self)
        action.triggered.connect(self.on_click_load_model)
        self.app_toolbar.addAction(action)
        self.app_toolbar.addSeparator()

        self.addToolBar(Qt.ToolBarArea.TopToolBarArea, self.app_toolbar)

    # def bind_event(self):
    #     self.loading_model_btn.clicked.connect(self.on_click_loading_model)
    #     self.loading_parameters_btn.clicked.connect(self.on_click_loading_parameters)
    #     self.select_account_btn.clicked.connect(self.on_click_select_account)
    #     self.btn_refresh.clicked.connect(self.on_refresh)

    #     # self.tab_widget_browser.tabBar().setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
    #     # self.tab_widget_browser.tabBar().customContextMenuRequested.connect(self.on_showContextMenu)

    # def init_default_status(self):
    #     self.selected_model_idx = -1
    #     self.selected_account_idx = -1

    def on_click_load_model(self):
        id = SelectModelDialog(self).exec()
        if id == QDialog.DialogCode.Rejected:
            return
        else:
            self.create_model_panel(id)

    def create_model_panel(self, model_id):
        model = ModelFactory().get_model(model_id)
        model_dock = MainDock(model.name, model.id, self.app_engine)
        self.addDockWidget(Qt.DockWidgetArea.TopDockWidgetArea, model_dock, Qt.Orientation.Vertical)

    # def on_click_loading_parameters(self):
    #     filename, _ = QFileDialog.getOpenFileName(self, "选择参数文件", r".", "参数文件(*.pth)")
    #     if filename is not None and len(filename) > 0:
    #         ModelFactory.load_data(filename)
    #         config = ModelFactory.get_config_dict()
    #         if config is not None:
    #             s = ""
    #             max_len = 0
    #             for key in config.keys():
    #                 if len(key) > max_len:
    #                     max_len = len(key)
    #             for key, value in config.items():
    #                 s = s + f"{key:<{max_len+1}}: {value}\n"

    #             self.config_info_textbrowser.setText(s)

    # self.ledit_filepath.setText(filename + ";" + filetypelist)

    # elif btn_clicked == QMessageBox.ButtonRole.RejectRole:
    #     print("操作二或取消被点击")
    # sid = self.webview_bbin.get_sid()
    # print(sid)

    # def on_click_select_account(self):
    #     dlg = SelectAccountDialog()
    #     select_idx = dlg.exec()
    #     if select_idx >= 0 and self.selected_account_idx != select_idx:
    #         self.account_name_label.setText(Accounts.data[select_idx]["Name"])
    #         self.binance = BinanceAccount(name=Accounts.data[select_idx]["Name"], apikey=Accounts.data[select_idx]["ApiKey"], secretkey=Accounts.data[select_idx]["SecertKey"])
    #         self.binance.getAssetBalance("USDT")

    #         self.selected_account_idx = select_idx

    # def on_refresh(self):
    #     url = self.lineedit_url.text()
    #     self.webview_bbin.load(QUrl(url))

    # def on_showContextMenu(self, pos):
    #     index = self.tab_widget_browser.tabBar().tabAt(pos)
    #     if index <= 0:
    #         return

    #     menu = QMenu(self.tab_widget_browser)
    #     action_close = QAction("关闭", self.tab_widget_browser)
    #     action_close.triggered.connect(lambda: self.tab_widget_browser.removeTab(index))
    #     menu.addAction(action_close)
    #     menu.exec(self.tab_widget_browser.tabBar().mapToGlobal(pos))

    # def add_tab(self, widget):
    #     print(1111)
    #     print(widget)
    #     self.tab_widget_browser.addTab(widget, "欧博游戏B")

    def closeEvent(self, event):
        """重写 QMainWindow::closeEvent"""
        reply = QMessageBox.question(self, "退出", "确认退出？", QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No, QMessageBox.StandardButton.No)
        if reply == QMessageBox.StandardButton.Yes:
            # self._save_dashboard_state("custom")
            # for app_win in self._apps_window.values():
            #     app_win.close()

            self.app_engine.close()
            event.accept()
            QApplication.quit()
        else:
            event.ignore()
