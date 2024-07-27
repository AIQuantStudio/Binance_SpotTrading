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
from main_frame import MainFrame

css_loading_model_on = """
            QPushButton {
                color:white;
                padding:8px 10px;
                background-color:#67C23A;
                border-radius:3px;
                font-size:14px
            }
            QPushButton:hover {
                color: #efefef;
                background: #57b22A;
            }
        """


switch_on_css_list = [
    "color:white",
    "padding:8px 10px",
    "background-color:#67C23A",
    "border-radius:3px",
    "font-size:14px",
]

switch_off_css_list = [
    "color:white",
    "padding:8px 10px",
    "background-color:#F56C6C",
    "border-radius:3px",
    "font-size:14px",
]

switch_disable_css_list = [
    "color:white",
    "padding:8px 10px",
    "background-color:#aaaaaa",
    "border-radius:3px",
    "font-size:14px",
]


class MainWindow(QMainWindow):

    def __init__(self, app_title, app_engine):
        super().__init__()
        
        self.webview_bbin = None
        self.app_engine = app_engine
        
        self.setWindowTitle(app_title)
        self.setup_ui()
        # self.bind_event()
        
        self.init_default_status()

        # 添加组件
        self.table_widget = None
        self.tab_widget = None

        self.log_widget = None
        self.record_widget = None
        self.l_name = None
        self.betRatio = None
        self.maxBetVal = None
        self.minBetVal = None
        self.l_game_url = None
        self.l_admin_url = None
        self.new_table_widget = None
        self.his_table_widget = None

        # 定义平台对象
        self.bbin_browser = None

        # 定义互斥锁
        # self.q_lock = QMutex()

        # 下注数据列表
        self.betInfoData = None
        self.betDataList = []

        # 开启下注时间
        self.startBetTime = None
        # 结束下注时间
        self.endBetTime = None

        # self.initFun()

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
        
        action = QAction(QIcon(QPixmap("./editor.ico")), '加载模型', self)
        action.triggered.connect(self.on_click_load_model)
        self.app_toolbar.addAction(action)
        self.app_toolbar.addSeparator()
        
        self.addToolBar(Qt.ToolBarArea.TopToolBarArea, self.app_toolbar)

        

        
        
        # sep_idx = 0
        # separator = Setting.get_global_setting("layout.main.apps", [])
        # if not bool(separator):
        #     separator = [len(self._apps_open_window)]

        # for i in range(len(self._apps_open_window)):
        #     if i == separator[sep_idx]:
        #         self._app_toolbar.addSeparator()
        #         sep_idx += 1 if sep_idx < len(separator) - 1 else 0

        #     func = self._apps_open_window[i]
        #     path = self._apps_icon_path[i]
        #     name = self._apps_display_name[i]

        #     icon = QtGui.QIcon()
        #     icon.addPixmap(QtGui.QPixmap(path))
        #     icon.addPixmap(QtGui.QPixmap(path), QtGui.QIcon.Disabled)
        #     icon.addPixmap(QtGui.QPixmap(path), QtGui.QIcon.Active)

        #     action = QtWidgets.QAction(name, self)
        #     action.triggered.connect(func)
        #     action.setIcon(icon)
        #     # action.setDisabled(True)

        #     self._app_toolbar.addAction(action)
        #     self._app_toolbar.setStyleSheet(
        #         "QToolButton:disabled {background-color:transparent}"
        #         "QToolButton:hover {background-color:lightgray}"
        #     )


        self.app_status_bar = QStatusBar()
        self.setStatusBar(self.app_status_bar)


        
   

        

        # main_widget = QWidget()
        # main_hbox_layout = QHBoxLayout()
        # main_widget.setLayout(main_hbox_layout)

        # main_left_widget = QWidget()
        # main_hbox_layout.addWidget(main_left_widget, stretch=2)

        # main_right_widget = QWidget()
        # main_hbox_layout.addWidget(main_right_widget, stretch=10)

        # self.setup_left_area_ui(main_left_widget)
        # self.setup_right_area_ui(main_right_widget)

        # self.setCentralWidget(main_widget)
        
        # self.setCentralWidget(self.log_dock)

    def setup_left_area_ui(self, widget: QWidget):
        vbox_layout = QVBoxLayout()

        model_frame = QFrame(self)
        model_frame.setFrameShape(QFrame.Shape.StyledPanel)
        binance_frame = QFrame(self)
        binance_frame.setFrameShape(QFrame.Shape.StyledPanel)
        
        model_vbox_layout = QVBoxLayout()
        binance_vbox_layout = QVBoxLayout()
        model_frame.setLayout(model_vbox_layout)
        binance_frame.setLayout(binance_vbox_layout)
        
        
        self.line = QFrame(self)
        self.line.setGeometry(QRect(0, 120, 341, 20))
        self.line.setFrameShadow(QFrame.Shadow.Sunken)
        self.line.setLineWidth(5)
        self.line.setFrameShape(QFrame.Shape.HLine)

        splitter = QSplitter(Qt.Orientation.Vertical)
        splitter.addWidget(model_frame)
        splitter.addWidget(self.line)
        splitter.addWidget(binance_frame)
        vbox_layout.addWidget(splitter)
        
        first_hbox_layout = QHBoxLayout()
        # 载入模型按钮
        self.loading_model_btn = QPushButton("选择模型")
        self.loading_model_btn.setFixedHeight(30)
        self.loading_model_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.loading_model_btn.setStyleSheet("QPushButton:hover { color: #333; }")
        # self.loading_model_btn.setStyleSheet(css_loading_model_on)
        self.loading_model_btn.setFixedWidth(100)
        first_hbox_layout.addWidget(self.loading_model_btn)
        # 模型名称标签
        self.model_name_label = QLabel("")
        first_hbox_layout.addWidget(self.model_name_label)
        model_vbox_layout.addLayout(first_hbox_layout)
    
        # 加载参数按钮
        self.loading_parameters_btn = QPushButton("加载参数")
        self.loading_parameters_btn.setFixedHeight(30)
        self.loading_parameters_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        # self.loading_parameters_btn.setStyleSheet(css_loading_model_on)
        self.loading_parameters_btn.setFixedWidth(100)
        self.loading_parameters_btn.setDisabled(True)
        model_vbox_layout.addWidget(self.loading_parameters_btn)
        
        # 交易对 GPU
        second_hbox_layout = QHBoxLayout()
        second_left_widget = QWidget()
        second_hbox_layout.addWidget(second_left_widget, stretch=8)
        second_right_widget = QWidget()
        second_hbox_layout.addWidget(second_right_widget, stretch=3)
        
        second_left_hbox_layout = QHBoxLayout()
        pair_name_label = QLabel("交易对: ")
        second_left_hbox_layout.addWidget(pair_name_label)
        self.pair_name_LineEdit = QLineEdit()
        self.pair_name_LineEdit.setEnabled(False)
        second_left_hbox_layout.addWidget(self.pair_name_LineEdit)
        second_left_widget.setLayout(second_left_hbox_layout)
        
        second_right_hbox_layout = QHBoxLayout()
        self.is_gpu_checkbox = QCheckBox("GPU")
        self.is_gpu_checkbox.setDisabled(True)
        second_right_hbox_layout.addWidget(self.is_gpu_checkbox)
        second_right_widget.setLayout(second_right_hbox_layout)
        
        model_vbox_layout.addLayout(second_hbox_layout)
        
        
        # 配置信息
        config_info_label = QLabel("配置信息：")
        model_vbox_layout.addWidget(config_info_label)
        self.config_info_textbrowser = QTextBrowser()
        self.config_info_textbrowser.setFont(QFont('Courier New'))
        model_vbox_layout.addWidget(self.config_info_textbrowser)
        
        ##################################################
        
        
        binance_first_hbox_layout = QHBoxLayout()
        # 选择账号
        self.select_account_btn = QPushButton("选择账号")
        self.select_account_btn.setFixedHeight(30)
        self.select_account_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.select_account_btn.setStyleSheet("QPushButton:hover { color: #333; }")
        # self.loading_model_btn.setStyleSheet(css_loading_model_on)
        self.select_account_btn.setFixedWidth(100)
        binance_first_hbox_layout.addWidget(self.select_account_btn)
        # 模型名称标签
        self.account_name_label = QLabel("")
        binance_first_hbox_layout.addWidget(self.account_name_label)
        binance_vbox_layout.addLayout(binance_first_hbox_layout)
        

        # 开始按钮
        self.btn_switch = QPushButton("开始监控")
        self.btn_switch.setFixedHeight(30)
        self.btn_switch.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_switch.setStyleSheet(";".join(switch_on_css_list))
        binance_vbox_layout.addWidget(self.btn_switch)

        # 下注上限
        h_box_Layout = QHBoxLayout()
        lbl_name = QLabel("下注上限")
        h_box_Layout.addWidget(lbl_name, 3)
        self.maxBetVal = QLineEdit("1")
        h_box_Layout.addWidget(self.maxBetVal, 9)
        binance_vbox_layout.addLayout(h_box_Layout)

        # 日志
        lbl_output_log = QLabel("日志：")
        binance_vbox_layout.addWidget(lbl_output_log)
        self.txtbrowser_output_log = QTextBrowser()
        binance_vbox_layout.addWidget(self.txtbrowser_output_log)

        widget.setLayout(vbox_layout)

    def setup_right_area_ui(self, widget: QWidget):
        v_layout = QVBoxLayout()

        widget_control_bar = QWidget()
        v_layout.addWidget(widget_control_bar, stretch=1)
        h_layout = QHBoxLayout()
        widget_control_bar.setLayout(h_layout)
        self.btn_refresh = QPushButton()
        self.btn_refresh.setText("刷新")
        h_layout.addWidget(self.btn_refresh, 1)

        self.lineedit_url = QLineEdit()
        self.lineedit_url.setFixedHeight(26)
        self.lineedit_url.setAlignment(Qt.AlignmentFlag.AlignVCenter)
        self.lineedit_url.setText(str(Config_Data.get("Url")))
        self.lineedit_url.setTextMargins(6, 0, 0, 0)
        self.lineedit_url.setFont(QFont("Arial", 16, QFont.Weight.Light))
        h_layout.addWidget(self.lineedit_url, 9)

        self.button_sid = QPushButton()
        self.button_sid.setText("获取Sid")
        h_layout.addWidget(self.button_sid, 1)

        # self.tab_widget_browser = QTabWidget()

        # tab_widget_browser.setStyleSheet("background-color:red;")

        # # 欧泊游戏平台
        # self.webview_bbin = QWebEngineView()
        # self.interceptor = BBINRequestInterceptor()
        # self.profile = QWebEngineProfile()
        # self.profile.setUrlRequestInterceptor(self.interceptor)
        # self.page = BBINWebEnginePage(self.profile, self.webview_bbin)

        self.scheme01 = QWebEngineUrlScheme(b"http")
        self.scheme01.setDefaultPort(80)
        QWebEngineUrlScheme.registerScheme(self.scheme01)

        self.scheme02 = QWebEngineUrlScheme(b"https")
        self.scheme02.setDefaultPort(443)
        QWebEngineUrlScheme.registerScheme(self.scheme02)

        # self.handler = BBINWebsocketSchemeHandler()

        # self.profile.installUrlSchemeHandler(b"http", self.handler)
        # self.profile.installUrlSchemeHandler(b"https", self.handler)

        # self.page.setUrl(QUrl(Config_Data.get("Url")))
        # self.webview_bbin.setPage(self.page)

        # self.webview_bbin.load(QUrl(Config_Data.get("Url")))

        v_layout.addWidget(self.webview_bbin, stretch=9)

        widget.setLayout(v_layout)

    def bind_event(self):
        self.loading_model_btn.clicked.connect(self.on_click_loading_model)
        self.loading_parameters_btn.clicked.connect(self.on_click_loading_parameters)
        self.select_account_btn.clicked.connect(self.on_click_select_account)
        self.btn_refresh.clicked.connect(self.on_refresh)

        # self.tab_widget_browser.tabBar().setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        # self.tab_widget_browser.tabBar().customContextMenuRequested.connect(self.on_showContextMenu)

    def init_default_status(self):
        self.selected_model_idx = -1
        self.selected_account_idx = -1


    def on_click_load_model(self):
        id = SelectModelDialog(self).exec()        
        if id == QDialog.DialogCode.Rejected:
            return
        else:
            self.create_model_panel(id)

            
    def create_model_panel(self, model_id):
        model = ModelFactory.get_model(model_id)
        panel = MainFrame(self, self.app_engine)
        dock_panel = QDockWidget(model.name)
        dock_panel.setObjectName(str(model.id))
        dock_panel.setFeatures(QDockWidget.DockWidgetFeature.DockWidgetClosable | QDockWidget.DockWidgetFeature.DockWidgetFloatable | QDockWidget.DockWidgetFeature.DockWidgetMovable)
        dock_panel.setAllowedAreas(Qt.DockWidgetArea.TopDockWidgetArea | Qt.DockWidgetArea.BottomDockWidgetArea )
        dock_panel.setWidget(panel)
        self.addDockWidget(Qt.DockWidgetArea.TopDockWidgetArea, dock_panel, Qt.Orientation.Vertical)
            
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
        
    
        
    def on_click_select_account(self):
        dlg = SelectAccountDialog()
        select_idx = dlg.exec()
        if select_idx >= 0 and self.selected_account_idx != select_idx:
            self.account_name_label.setText(Accounts.data[select_idx]["Name"])
            self.binance = BinanceAccount(name=Accounts.data[select_idx]["Name"], apikey=Accounts.data[select_idx]["ApiKey"], secretkey=Accounts.data[select_idx]["SecertKey"])
            self.binance.getAssetBalance("USDT")
            
            self.selected_account_idx = select_idx

    def on_refresh(self):
        url = self.lineedit_url.text()
        self.webview_bbin.load(QUrl(url))

    def on_showContextMenu(self, pos):
        index = self.tab_widget_browser.tabBar().tabAt(pos)
        if index <= 0:
            return

        menu = QMenu(self.tab_widget_browser)
        action_close = QAction("关闭", self.tab_widget_browser)
        action_close.triggered.connect(lambda: self.tab_widget_browser.removeTab(index))
        menu.addAction(action_close)
        menu.exec(self.tab_widget_browser.tabBar().mapToGlobal(pos))

    def add_tab(self, widget):
        print(1111)
        print(widget)
        self.tab_widget_browser.addTab(widget, "欧博游戏B")

    def closeEvent(self, event):
        """ 重写 QMainWindow::closeEvent """
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