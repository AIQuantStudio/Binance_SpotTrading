from PyQt6.QtCore import *
from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
from PyQt6.QtWebEngineWidgets import QWebEngineView
from PyQt6.QtWebEngineCore import QWebEngineProfile, QWebEngineUrlScheme

# from views.bbin_webengine_view import BBINWebEngineView
# from core.bbin_request_interceptor import BBINRequestInterceptor
# from core.bbin_webengine_page import BBINWebEnginePage
# from core.bbin_ws_scheme_handler import BBINWebsocketSchemeHandler
# from views.adminWebEngine import AdminWebEngine
from config import Config_Data
from select_model_dialog import CustomDialog


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

    def __init__(self, title):
        super().__init__()

        self.webview_bbin = None

        self.setWindowTitle(title)
        self.setup_ui()
        self.bind_event()

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

        main_widget = QWidget()
        main_hbox_layout = QHBoxLayout()
        main_widget.setLayout(main_hbox_layout)

        main_left_widget = QWidget()
        main_hbox_layout.addWidget(main_left_widget, stretch=2)

        main_right_widget = QWidget()
        main_hbox_layout.addWidget(main_right_widget, stretch=10)

        self.setup_left_area_ui(main_left_widget)
        self.setup_right_area_ui(main_right_widget)

        self.setCentralWidget(main_widget)

    def setup_left_area_ui(self, widget: QWidget):
        vbox_layout = QVBoxLayout()

        # 载入模型按钮
        self.loading_model_btn = QPushButton("模型")
        self.loading_model_btn.setFixedHeight(30)
        self.loading_model_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.loading_model_btn.setStyleSheet(css_loading_model_on)
        self.loading_model_btn.setFixedWidth(100)
        # self.loading_model_btn.setDisabled(True)
        vbox_layout.addWidget(self.loading_model_btn)
        
        
        # 加载参数按钮
        self.loading_parameters_btn = QPushButton("加载参数")
        self.loading_parameters_btn.setFixedHeight(30)
        self.loading_parameters_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.loading_parameters_btn.setStyleSheet(css_loading_model_on)
        self.loading_parameters_btn.setFixedWidth(100)
        # self.loading_model_btn.setDisabled(True)
        vbox_layout.addWidget(self.loading_parameters_btn)

        # 开始按钮
        self.btn_switch = QPushButton("开始监控")
        self.btn_switch.setFixedHeight(30)
        self.btn_switch.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_switch.setStyleSheet(";".join(switch_on_css_list))
        vbox_layout.addWidget(self.btn_switch)

        # 下注上限
        h_box_Layout = QHBoxLayout()
        lbl_name = QLabel("下注上限")
        h_box_Layout.addWidget(lbl_name, 3)
        self.maxBetVal = QLineEdit("1")
        h_box_Layout.addWidget(self.maxBetVal, 9)
        vbox_layout.addLayout(h_box_Layout)

        # 信息
        lbl_output_info = QLabel("信息：")
        vbox_layout.addWidget(lbl_output_info)
        self.txtbrowser_output_info = QTextBrowser()
        vbox_layout.addWidget(self.txtbrowser_output_info)

        # 日志
        lbl_output_log = QLabel("日志：")
        vbox_layout.addWidget(lbl_output_log)
        self.txtbrowser_output_log = QTextBrowser()
        vbox_layout.addWidget(self.txtbrowser_output_log)

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
        # self.btn_switch.clicked.connect(self.onClickWatchButton)
        self.loading_model_btn.clicked.connect(self.on_click)
        self.loading_parameters_btn.clicked.connect(self.on_click_loading_parameters)
        self.btn_refresh.clicked.connect(self.on_refresh)

        # self.tab_widget_browser.tabBar().setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        # self.tab_widget_browser.tabBar().customContextMenuRequested.connect(self.on_showContextMenu)

    def on_click_loading_parameters(self):
        filename, _ = QFileDialog.getOpenFileName(self, "Open File", r".", "参数文件(*.py)")
        print(filename)
        # self.ledit_filepath.setText(filename + ";" + filetypelist)


    def on_click(self):
        msg = CustomDialog()
        
        btn_clicked = msg.exec()
        print(btn_clicked)
        print(QMessageBox.ButtonRole.AcceptRole)
        print(QMessageBox.ButtonRole.RejectRole)
        if btn_clicked == QMessageBox.ButtonRole.AcceptRole:
            print("操作一被点击")
        elif btn_clicked == QMessageBox.ButtonRole.RejectRole:
            print("操作二或取消被点击")
        # sid = self.webview_bbin.get_sid()
        # print(sid)

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
