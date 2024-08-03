from PyQt6.QtCore import *
from PyQt6.QtWidgets import *
from PyQt6.QtGui import *

from frame import AssetBalancePenal, TradeSettingPenal, TradeHistoryMonitor
from select_account_dialog import SelectAccountDialog

class TradePanel(QFrame):

    def __init__(self, parent_widget, top_dock, app_engine):
        super().__init__(parent_widget)

        self.top_dock = top_dock
        self.app_engine = app_engine

        self.setup_ui()
        self.bind_event()

    def setup_ui(self):
        main_hbox_layout = QHBoxLayout()
        self.setLayout(main_hbox_layout)

        main_left_widget = QWidget()
        main_hbox_layout.addWidget(main_left_widget, stretch=3)

        main_middle_widget = QWidget()
        main_hbox_layout.addWidget(main_middle_widget, stretch=3)
        
        main_right_widget = QWidget()
        main_hbox_layout.addWidget(main_right_widget, stretch=5)

        self.setup_left_area_ui(main_left_widget)
        self.setup_middle_area_ui(main_middle_widget)
        self.setup_right_area_ui(main_right_widget)

    def setup_left_area_ui(self, left_widget):
        vbox_layout = QVBoxLayout()
        left_widget.setLayout(vbox_layout)

        self.select_account_btn = QPushButton()
        self.select_account_btn.setText("选择账号")
        vbox_layout.addWidget(self.select_account_btn)
        
        self.asset_balance_panel = AssetBalancePenal(self, self.top_dock, self.app_engine)
        vbox_layout.addWidget( self.asset_balance_panel)

    def setup_middle_area_ui(self, middle_widget):
        vbox_layout = QVBoxLayout()
        middle_widget.setLayout(vbox_layout)
        
        self.trade_setting_panel = TradeSettingPenal(self, self.top_dock, self.app_engine)
        vbox_layout.addWidget( self.trade_setting_panel)
        
        self.start_trade_btn = QPushButton()
        self.start_trade_btn.setText("启动交易")
        vbox_layout.addWidget(self.start_trade_btn)

        # self.select_account_btn = QPushButton()
        # self.select_account_btn.setText("选择账号")
        # vbox_layout.addWidget(self.select_account_btn)
        
        # self.asset_balance_panel = AssetBalancePenal(self, self.top_dock, self.app_engine)
        # vbox_layout.addWidget( self.asset_balance_panel)
        
    def setup_right_area_ui(self, right_widget):
        vbox_layout = QVBoxLayout()
        right_widget.setLayout(vbox_layout)
        
        self.trade_history_monitor = TradeHistoryMonitor(self, self.top_dock, self.app_engine)
        vbox_layout.addWidget(self.trade_history_monitor)
        
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
        
    def bind_event(self):
        self.select_account_btn.clicked.connect(self.on_click_select_account)
        
    def on_click_select_account(self):
        ret = SelectAccountDialog(self, self.top_dock.id).exec()
        if ret == QDialog.DialogCode.Accepted:
            self.load_trade_panel()
    
    def load_trade_panel(self):
        
    def close(self):
        return super().close()