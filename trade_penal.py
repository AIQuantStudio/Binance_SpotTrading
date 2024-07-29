from PyQt6.QtCore import *
from PyQt6.QtWidgets import *
from PyQt6.QtGui import *


class TradePanel(QFrame):

    def __init__(self, parent_widget, top_dock, app_engine):
        super().__init__(parent_widget)

        self.top_dock = top_dock
        self.app_engine = app_engine

        self.setup_ui()

    def setup_ui(self):
        main_hbox_layout = QHBoxLayout()
        self.setLayout(main_hbox_layout)

        main_left_widget = QWidget()
        main_hbox_layout.addWidget(main_left_widget, stretch=3)

        main_right_widget = QWidget()
        main_hbox_layout.addWidget(main_right_widget, stretch=10)

        self.setup_left_area_ui(main_left_widget)
        self.setup_right_area_ui(main_right_widget)

    def setup_left_area_ui(self, left_widget):
        vbox_layout = QVBoxLayout()

        symbol_label = QLabel("交易对: ")
        vbox_layout.addWidget(symbol_label)

        config_info_label = QLabel("配置信息：")
        vbox_layout.addWidget(config_info_label)

        self.config_info_textbrowser = QTextBrowser()
        self.config_info_textbrowser.setFont(QFont("Courier New"))
        vbox_layout.addWidget(self.config_info_textbrowser)

        left_widget.setLayout(vbox_layout)

    def setup_right_area_ui(self, right_widget):
        vbox_layout = QVBoxLayout()

        # widget_control_bar = QWidget()
        # vbox_layout.addWidget(widget_control_bar, stretch=1)
        # h_layout = QHBoxLayout()
        # widget_control_bar.setLayout(h_layout)
        # self.btn_refresh = QPushButton()
        # self.btn_refresh.setText("刷新")
        # h_layout.addWidget(self.btn_refresh, 1)

        # self.button_sid = QPushButton()
        # self.button_sid.setText("获取Sid")
        # h_layout.addWidget(self.button_sid, 1)

        # vbox_layout.addLayout(h_layout)

        right_widget.setLayout(vbox_layout)
