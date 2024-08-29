from PyQt6.QtCore import *
from PyQt6.QtWidgets import *
from PyQt6.QtGui import *

from main_engine import MainEngine
from model import ModelFactory
from account import AccountFactory
from trading import TradingFactory, TradingDaemon
from strategy import StrategyFactory
from widget.log_monitor import LogMonitor
from widget.market_canvas import MarketCanvas
from widget.asset_balance_table import AssetBalanceTable
from widget.trade_history_table import TradeHistoryMonitor
from widget.select_account_dialog import SelectAccountDialog
from widget.trade_setting.trade_setting_interface import TradeSettingInterface
from widget.trade_setting.empty_trade_setting_panel import EmptyTradeSettingPanel
from widget.trade_setting.normal_trade_setting_panel import NormalTradeSettingPanel
from widget.trade_setting.test_trade_setting_panel import TestTradeSettingPanel
from structure import TradeMode, AssetBalanceData, LogStruct, TradeSettingStruct
from event import Event, EVENT_ASSET_BALANCE, EVENT_LOG


class AppWin(QFrame):

    def __init__(self, parent_widget, app_id):
        super().__init__(parent_widget)

        self.app_id = app_id
        self.mode = TradeMode.EMPTY

        self.setup_ui()
        self.bind_event()

        self.show_model_info()
        self.show_market()

    def setup_ui(self):
        self.setLineWidth(1)
        self.setMidLineWidth(1)
        self.setFrameStyle(QFrame.Shape.Box | QFrame.Shadow.Sunken)

        vbox_layout = QVBoxLayout()
        vbox_layout.setContentsMargins(5, 0, 0, 0)
        self.setLayout(vbox_layout)

        self.setup_ui_upper_half(vbox_layout)

        self.line = QFrame(self)
        self.line.setGeometry(QRect(0, 120, 341, 20))
        self.line.setFrameShadow(QFrame.Shadow.Sunken)
        self.line.setLineWidth(5)
        self.line.setFrameShape(QFrame.Shape.HLine)
        vbox_layout.addWidget(self.line)

        self.setup_ui_lower_half(vbox_layout)

    def setup_ui_upper_half(self, layout: QVBoxLayout):
        hbox_layout = QHBoxLayout()
        layout.addLayout(hbox_layout, stretch=6)

        left_widget = QWidget()
        hbox_layout.addWidget(left_widget, stretch=3)

        right_widget = QWidget()
        hbox_layout.addWidget(right_widget, stretch=10)

        self.setup_ui_upper_half_left_area(left_widget)
        self.setup_ui_upper_half_right_area(right_widget)

    def setup_ui_upper_half_left_area(self, left_widget: QWidget):
        vbox_layout = QVBoxLayout()

        config_info_label = QLabel("配置信息")
        vbox_layout.addWidget(config_info_label)

        self.config_info_textbrowser = QTextBrowser()
        self.config_info_textbrowser.setFont(QFont("Courier New", 11))
        self.config_info_textbrowser.setMaximumHeight(200)
        vbox_layout.addWidget(self.config_info_textbrowser)

        vertical_sep_line = QFrame(left_widget)
        vertical_sep_line.setLineWidth(8)
        vertical_sep_line.setFrameShape(QFrame.Shape.HLine)
        vertical_sep_line.setFrameShadow(QFrame.Shadow.Sunken)
        vbox_layout.addWidget(vertical_sep_line)

        self.log_monitor = LogMonitor(self, self.app_id)
        vbox_layout.addWidget(self.log_monitor)

        left_widget.setLayout(vbox_layout)

    def setup_ui_upper_half_right_area(self, right_widget: QWidget):
        vbox_layout = QVBoxLayout()
        right_widget.setLayout(vbox_layout)

        self.market_canvas = MarketCanvas(self, self.app_id)
        vbox_layout.addWidget(self.market_canvas)

    def setup_ui_lower_half(self, layout: QVBoxLayout):
        hbox_layout = QHBoxLayout()
        layout.addLayout(hbox_layout, stretch=4)

        left_widget = QWidget()
        hbox_layout.addWidget(left_widget, stretch=3)

        middle_widget = QWidget()
        hbox_layout.addWidget(middle_widget, stretch=3)

        right_widget = QWidget()
        hbox_layout.addWidget(right_widget, stretch=5)

        self.setup_ui_lower_half_left_area(left_widget)
        self.setup_ui_lower_half_middle_area(middle_widget)
        self.setup_ui_lower_half_right_area(right_widget)

    def setup_ui_lower_half_left_area(self, left_widget: QWidget):
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

        self.asset_balance_table = AssetBalanceTable(self, self.app_id)
        vbox_layout.addWidget(self.asset_balance_table)

        self.show_all_balance_checkbox = QCheckBox()
        self.show_all_balance_checkbox.setText("显示全部")
        self.show_all_balance_checkbox.setCheckState(Qt.CheckState.Checked)
        self.show_all_balance_checkbox.setDisabled(True)
        vbox_layout.addWidget(self.show_all_balance_checkbox)

    def setup_ui_lower_half_middle_area(self, middle_widget: QWidget):
        vbox_layout = QVBoxLayout()
        middle_widget.setLayout(vbox_layout)

        self.stacked_setting_panel = QStackedWidget(middle_widget)

        self.stacked_setting_panel.addWidget(EmptyTradeSettingPanel(self, self.app_id))
        self.stacked_setting_panel.addWidget(NormalTradeSettingPanel(self, self.app_id))
        self.stacked_setting_panel.addWidget(TestTradeSettingPanel(self, self.app_id))

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

    def setup_ui_lower_half_right_area(self, right_widget: QWidget):
        vbox_layout = QVBoxLayout()
        right_widget.setLayout(vbox_layout)

        self.trade_history_monitor = TradeHistoryMonitor(self, self.app_id)
        vbox_layout.addWidget(self.trade_history_monitor)

        right_widget.setLayout(vbox_layout)

    def bind_event(self):
        self.select_account_btn.clicked.connect(self.on_click_select_account)
        self.remove_account_btn.clicked.connect(self.on_click_remove_account)
        self.show_all_balance_checkbox.stateChanged.connect(self.refresh_asset_balance)
        self.start_trade_btn.clicked.connect(self.on_click_start_trade)
        self.stop_trade_btn.clicked.connect(self.on_click_stop_trade)

    def on_click_select_account(self):
        ret = SelectAccountDialog(self, self.app_id).exec()
        if ret == QDialog.DialogCode.Accepted:
            self.load_trade_panel_status()
            self.refresh_asset_balance()

    def on_click_remove_account(self):
        daemon : TradingDaemon = TradingFactory().get_daemon(self.app_id)
        if daemon is not None and daemon.is_running:
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
        setting_data: TradeSettingStruct = trade_setting.get_setting_data()

        # 模型参数
        model_config = ModelFactory().get_config_dict(self.app_id)
        strategy = StrategyFactory(setting_data.strategy_name)

        daemon = TradingFactory().create_daemon(self.app_id, self.mode, strategy, setting_data)
        daemon.start()

    def on_click_stop_trade(self):
        self.start_trade_btn.setEnabled(True)
        self.stop_trade_btn.setDisabled(True)

        trade_setting: TradeSettingInterface = self.stacked_setting_panel.currentWidget()
        trade_setting.unlock_all()

        daemon = TradingFactory().get_daemon(self.app_id)
        daemon.stop()

    def refresh_asset_balance(self):
        show_all = self.show_all_balance_checkbox.checkState() == Qt.CheckState.Checked
        balances = AccountFactory().get_asset_balance(self.app_id)
        currencies = ModelFactory().get_model_curreny(self.app_id)
        self.asset_balance_table.clear_contents()
        for balance in balances:
            if show_all == False:
                if balance["asset"].upper() not in currencies:
                    continue

            account_data = AssetBalanceData(currency=balance["asset"].upper(), free=float(balance["free"]), locked=float(balance["locked"]))
            MainEngine.event_engine.put(Event(EVENT_ASSET_BALANCE, account_data))

    def load_trade_panel_status(self):
        self.account_label.setText(AccountFactory().get_name(self.app_id))
        self.show_all_balance_checkbox.setEnabled(True)
        self.start_trade_btn.setEnabled(True)
        self.stop_trade_btn.setEnabled(False)
        self.remove_account_btn.setVisible(True)
        self.select_account_btn.setVisible(False)

        if AccountFactory().is_test(self.app_id):
            self.switch_trade_setting_panel(TradeMode.BACKTEST)
        else:
            self.switch_trade_setting_panel(TradeMode.NORMAL)

    def clear_trade_panel_status(self):
        self.account_label.setText("")
        self.show_all_balance_checkbox.setEnabled(False)
        self.start_trade_btn.setEnabled(False)
        self.stop_trade_btn.setEnabled(False)
        self.remove_account_btn.setVisible(False)
        self.select_account_btn.setVisible(True)

        self.asset_balance_table.clear_contents()
        self.switch_trade_setting_panel(TradeMode.EMPTY)

    def switch_trade_setting_panel(self, mode):
        self.mode = mode
        if self.mode == TradeMode.EMPTY:
            self.stacked_setting_panel.setCurrentIndex(0)

        elif self.mode == TradeMode.NORMAL:
            self.stacked_setting_panel.setCurrentIndex(1)

        elif self.mode == TradeMode.BACKTEST:
            self.stacked_setting_panel.setCurrentIndex(2)

    def show_model_info(self):
        config = ModelFactory().get_config_dict(self.app_id)
        if config is not None:
            s = ""
            max_len = 0
            for key in config.keys():
                if len(key) > max_len:
                    max_len = len(key)
            for key, value in config.items():
                s = s + f"{key:<{max_len+1}}: {value}\n"

            self.config_info_textbrowser.setText(s)

    def show_market(self):
        self.market_canvas.start_market()

    def close(self) -> bool:
        self.market_canvas.stop_market()
        self.log_monitor.close()
        # self.model_panel.close()

        self.asset_balance_table.close()
        # self.trade_panel.close()
        return super().close()

    def write_log(self, msg):
        MainEngine.write_log(msg)
        MainEngine.event_engine.put(event=Event(EVENT_LOG, LogStruct(msg=msg)), suffix=self.app_id)
