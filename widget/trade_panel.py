from PyQt6.QtCore import *
from PyQt6.QtWidgets import *
from PyQt6.QtGui import *

from widget.asset_balance_table import AssetBalanceTable

from widget.trade_history_table import TradeHistoryMonitor
from widget import SelectAccountDialog
from widget.trade_setting.trade_setting_interface import TradeSettingInterface
from widget.trade_setting.empty_trade_setting_panel import EmptyTradeSettingPanel
from widget.trade_setting.normal_trade_setting_panel import NormalTradeSettingPanel
from widget.trade_setting.test_trade_setting_panel import TestTradeSettingPanel

from structure import TradeSettingMode, AssetBalanceData

# from exchange import BinanceFactory
from app_engine import AppEngine
from account import AccountFactory
from model import ModelFactory
from trading import TradingFactory
from event import Event, EVENT_ASSET_BALANCE, EVENT_LOG
from structure import LogStruct


class TradePanel(QFrame):

    def __init__(self, parent_widget, top_dock):
        super().__init__(parent_widget)

        self.top_dock = top_dock
        self.mode = TradeSettingMode.EMPTY

        self.setup_ui()
        self.bind_event()

    def setup_ui(self):
        main_hbox_layout = QHBoxLayout()
        self.setLayout(main_hbox_layout)

        self.main_left_widget = QWidget()
        main_hbox_layout.addWidget(self.main_left_widget, stretch=3)

        self.main_middle_widget = QWidget()
        main_hbox_layout.addWidget(self.main_middle_widget, stretch=3)

        self.main_right_widget = QWidget()
        main_hbox_layout.addWidget(self.main_right_widget, stretch=5)

        self.setup_left_area_ui(self.main_left_widget)
        self.setup_middle_area_ui(self.main_middle_widget)
        self.setup_right_area_ui(self.main_right_widget)

    def setup_left_area_ui(self, left_widget: QWidget):
        vbox_layout = QVBoxLayout()
        left_widget.setLayout(vbox_layout)

        hbox_layout = QHBoxLayout()
        hbox_layout.setContentsMargins(0, 0, 0, 0)
        vbox_layout.addLayout(hbox_layout)

        self.select_account_btn = QPushButton()
        self.select_account_btn.setText("选择账号")
        hbox_layout.addWidget(self.select_account_btn, stretch=4)

        self.remove_account_btn = QPushButton()
        self.remove_account_btn.setText("移除账号")
        self.remove_account_btn.setVisible(False)
        hbox_layout.addWidget(self.remove_account_btn, stretch=4)

        self.account_label = QLabel()
        self.account_label.setText("")
        hbox_layout.addWidget(self.account_label, stretch=6)

        self.asset_balance_table = AssetBalanceTable(self, self.top_dock)
        vbox_layout.addWidget(self.asset_balance_table)

        self.show_all_balance_checkbox = QCheckBox()
        self.show_all_balance_checkbox.setText("显示全部")
        self.show_all_balance_checkbox.setCheckState(Qt.CheckState.Checked)
        self.show_all_balance_checkbox.setDisabled(True)
        vbox_layout.addWidget(self.show_all_balance_checkbox)

    def setup_middle_area_ui(self, middle_widget: QWidget):
        vbox_layout = QVBoxLayout()
        middle_widget.setLayout(vbox_layout)

        self.stacked_setting_panel = QStackedWidget(middle_widget)

        self.stacked_setting_panel.addWidget(EmptyTradeSettingPanel(self, self.top_dock))
        self.stacked_setting_panel.addWidget(NormalTradeSettingPanel(self, self.top_dock))
        self.stacked_setting_panel.addWidget(TestTradeSettingPanel(self, self.top_dock))

        self.trade_setting_panel = self.switch_trade_setting_panel(self.mode)
        vbox_layout.addWidget(self.stacked_setting_panel)

        hbox_layout = QHBoxLayout()
        self.start_trade_btn = QPushButton()
        self.start_trade_btn.setText("启动交易")
        self.start_trade_btn.setDisabled(True)
        hbox_layout.addWidget(self.start_trade_btn)
        self.stop_trade_btn = QPushButton()
        self.stop_trade_btn.setText("停止交易")
        self.stop_trade_btn.setDisabled(True)
        hbox_layout.addWidget(self.stop_trade_btn)
        vbox_layout.addLayout(hbox_layout)

    def setup_right_area_ui(self, right_widget: QWidget):
        vbox_layout = QVBoxLayout()
        right_widget.setLayout(vbox_layout)

        self.trade_history_monitor = TradeHistoryMonitor(self, self.top_dock)
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
        self.remove_account_btn.clicked.connect(self.on_click_remove_account)
        self.show_all_balance_checkbox.stateChanged.connect(self.refresh_asset_balance)
        self.start_trade_btn.clicked.connect(self.on_click_start_trade)
        self.stop_trade_btn.clicked.connect(self.on_click_stop_trade)

        # AppEngine.event_engine.register(EVENT_TRADE_RECORD, self.event_trade_record)

    def on_click_select_account(self):
        ret = SelectAccountDialog(self, self.top_dock.id).exec()
        if ret == QDialog.DialogCode.Accepted:
            self.load_trade_panel_status()
            self.refresh_asset_balance()

    def on_click_remove_account(self):
        rule = TradeFactory().get_trade_rule(self.top_dock.id)
        if rule is None:
            self.clear_trade_panel_status()
            return

        if rule.is_running:
            QMessageBox.warning(self, "警告", f"账号正在交易运行，请先停止！", QMessageBox.StandardButton.Ok)
            return

        reply = QMessageBox.question(self, "移除账号", "确认移除账号？", QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No, QMessageBox.StandardButton.No)
        if reply == QMessageBox.StandardButton.Yes:
            self.clear_trade_panel_status()

    def on_click_start_trade(self):
        self.start_trade_btn.setDisabled(True)
        self.stop_trade_btn.setEnabled(True)
        
        # 交易设置
        trade_setting: TradeSettingInterface = self.stacked_setting_panel.currentWidget()
        trade_setting.lock_all()
        setting_data = trade_setting.get_setting_data()
        
        # 模型参数
        model_config = ModelFactory().get_config_dict(self.top_dock.id)
        strategy = Strategy()

        daemon = TradingFactory().create_daemon(self.top_dock.id, self.mode, strategy, setting_data)
        daemon.start()

    def on_click_stop_trade(self):
        self.start_trade_btn.setEnabled(True)
        self.stop_trade_btn.setDisabled(True)
        
        trade_setting: TradeSettingInterface = self.stacked_setting_panel.currentWidget()
        trade_setting.unlock_all()
        
        daemon = TradingFactory().get_daemon(self.top_dock.id)
        daemon.stop()

    def refresh_asset_balance(self):
        show_all = self.show_all_balance_checkbox.checkState() == Qt.CheckState.Checked
        balances = AccountFactory().get_asset_balance(self.top_dock.id)
        currencies = ModelFactory().get_model_curreny(self.top_dock.id)
        self.asset_balance_table.clear_contents()
        for balance in balances:
            if show_all == False:
                if balance["asset"].upper() not in currencies:
                    continue

            account_data = AssetBalanceData(currency=balance["asset"].upper(), free=float(balance["free"]), locked=float(balance["locked"]))
            AppEngine.event_engine.put(Event(EVENT_ASSET_BALANCE, account_data))

    def load_trade_panel_status(self):
        self.account_label.setText(AccountFactory().get_name(self.top_dock.id))
        self.show_all_balance_checkbox.setEnabled(True)
        self.start_trade_btn.setEnabled(True)
        self.stop_trade_btn.setEnabled(False)
        self.remove_account_btn.setVisible(True)
        self.select_account_btn.setVisible(False)

        if AccountFactory().is_test(self.top_dock.id):
            self.switch_trade_setting_panel(TradeSettingMode.TEST)
        else:
            self.switch_trade_setting_panel(TradeSettingMode.NORMAL)

    def clear_trade_panel_status(self):
        self.account_label.setText("")
        self.show_all_balance_checkbox.setEnabled(False)
        self.start_trade_btn.setEnabled(False)
        self.stop_trade_btn.setEnabled(False)
        self.remove_account_btn.setVisible(False)
        self.select_account_btn.setVisible(True)

        self.asset_balance_table.clear_contents()
        self.switch_trade_setting_panel(TradeSettingMode.EMPTY)

    def switch_trade_setting_panel(self, mode):
        self.mode = mode
        if self.mode == TradeSettingMode.EMPTY:
            self.stacked_setting_panel.setCurrentIndex(0)

        elif self.mode == TradeSettingMode.NORMAL:
            self.stacked_setting_panel.setCurrentIndex(1)

        elif self.mode == TradeSettingMode.TEST:
            self.stacked_setting_panel.setCurrentIndex(2)

    def event_trade_record(self, data):
        trade_data = data

    def close(self):
        self.asset_balance_table.close()
        return super().close()

    def write_log(self, msg):
        AppEngine.write_log(msg)
        AppEngine.event_engine.put(event = Event(EVENT_LOG, LogStruct(msg=msg)), suffix=self.top_dock.id)