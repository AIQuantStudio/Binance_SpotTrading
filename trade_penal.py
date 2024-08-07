from PyQt6.QtCore import *
from PyQt6.QtWidgets import *
from PyQt6.QtGui import *

from widget import AssetBalancePenal, TradeSettingPenal, TradeHistoryMonitor
from select_account_dialog import SelectAccountDialog
from exchange import BinanceFactory
from model import ModelFactory
from structure import AssetBalanceData
from event import Event, EVENT_ASSET_BALANCE

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

        hbox_layout = QHBoxLayout()
        hbox_layout.setContentsMargins(0,0,0,0)
        vbox_layout.addLayout(hbox_layout)
        
        self.select_account_btn = QPushButton()
        self.select_account_btn.setText("选择账号")
        hbox_layout.addWidget(self.select_account_btn, stretch=4)
        
        self.binance_account_label = QLabel()
        self.binance_account_label.setText("")
        hbox_layout.addWidget(self.binance_account_label, stretch=6)
        
        self.asset_balance_panel = AssetBalancePenal(self, self.top_dock, self.app_engine)
        vbox_layout.addWidget( self.asset_balance_panel)
        
        self.show_all_balance_checkbox = QCheckBox()
        self.show_all_balance_checkbox.setText("显示全部")
        self.show_all_balance_checkbox.setCheckState(Qt.CheckState.Checked)
        vbox_layout.addWidget( self.show_all_balance_checkbox)

    def setup_middle_area_ui(self, middle_widget):
        vbox_layout = QVBoxLayout()
        middle_widget.setLayout(vbox_layout)
        
        self.trade_setting_panel = TradeSettingPenal(self, self.top_dock, self.app_engine)
        vbox_layout.addWidget( self.trade_setting_panel)
        
        # self.start_trade_btn = QPushButton()
        # self.start_trade_btn.setText("启动交易")
        # vbox_layout.addWidget(self.start_trade_btn)
        
        
        hbox_layout = QHBoxLayout()
        self.start_trade_btn = QPushButton()
        self.start_trade_btn.setText("启动交易")
        hbox_layout.addWidget(self.start_trade_btn)
        self.stop_trade_btn = QPushButton()
        self.stop_trade_btn.setText("停止交易")
        self.stop_trade_btn.setDisabled(True)
        hbox_layout.addWidget(self.stop_trade_btn)
        vbox_layout.addLayout(hbox_layout)

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
        self.show_all_balance_checkbox.stateChanged.connect(self.on_show_all_balance_changed)
        
    def on_show_all_balance_changed(self):
        state = self.show_all_balance_checkbox.checkState()
        if state == Qt.CheckState.Unchecked:
            self.asset_balance_panel.clear_table()
            self.load_asset_balance_penal(False)
        else:
            self.asset_balance_panel.clear_table()
            self.load_asset_balance_penal(True)
        
    def on_click_select_account(self):
        ret = SelectAccountDialog(self, self.top_dock.id).exec()
        if ret == QDialog.DialogCode.Accepted:
            self.binance_account_label.setText(BinanceFactory().get_account_name(self.top_dock.id))
            self.load_asset_balance_penal()
    
    def load_asset_balance_penal(self, show_all = True):
        balances = BinanceFactory().get_asset_balance(self.top_dock.id)
        model = ModelFactory().get_model(self.top_dock.id)
        show_symbols = [model.base_currency, model.quote_currency]
        for balance in balances:
            if show_all == False:
                if balance["asset"] not in show_symbols:
                    continue
            
            account_data = AssetBalanceData(
                    symbol=balance["asset"],
                    free=float(balance["free"]),
                    locked=float(balance["locked"])
                )
            self.app_engine.event_engine.put(Event(EVENT_ASSET_BALANCE, account_data))
        
    def close(self):
        return super().close()