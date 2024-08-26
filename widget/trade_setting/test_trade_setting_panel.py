from PyQt6.QtCore import *
from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
from typing import Any
from datetime import datetime

from widget.trade_setting.trade_setting_interface import TradeSettingInterface
from model import ModelFactory
from structure import TestSettingStruct
from setting import StrategySetting


class TestTradeSettingPanel(QFrame, TradeSettingInterface):

    def __init__(self, parent_widget, top_dock):
        super().__init__(parent_widget)

        self.top_dock = top_dock

        self.setLineWidth(2)
        self.setMidLineWidth(2)
        self.setFrameStyle(QFrame.Shape.Panel | QFrame.Shadow.Sunken)

        vbox_layout = QVBoxLayout()
        self.setLayout(vbox_layout)

        self.predict_at_first_time_checkbox = QCheckBox()
        self.predict_at_first_time_checkbox.setToolTip("从启动时间开始预测")

        self.begin_datetime_edit = QDateTimeEdit()
        self.begin_datetime_edit.setDateTime(QDateTime(datetime(2024, 1, 1)))
        self.end_datetime_edit = QDateTimeEdit()
        self.end_datetime_edit.setDateTime(QDateTime(datetime(2024, 1, 2)))

        self.refer_currency_combobox = QComboBox()
        self.refer_currency_combobox.addItems([currency for currency in ModelFactory().get_model_curreny(self.top_dock.id)])
        self.refer_currency_combobox.setItemDelegate(QStyledItemDelegate())

        double_validator = QDoubleValidator()
        double_validator.setBottom(0)
        self.trade_amount_edit = QLineEdit()
        self.trade_amount_edit.setValidator(double_validator)
        self.trade_amount_edit.setText("100.0")
        
        self.strategy_name_combobox = QComboBox()
        self.strategy_name_combobox.addItems([strategy["Name"] for strategy in StrategySetting.Strategies])
        self.strategy_name_combobox.setItemDelegate(QStyledItemDelegate())


        grid = QGridLayout()
        grid.addWidget(QLabel("从启动时间开始预测"), 0, 0)
        grid.addWidget(QLabel("起始时间"), 1, 0)
        grid.addWidget(QLabel("终止时间"), 2, 0)
        grid.addWidget(QLabel("交易对象"), 3, 0)
        grid.addWidget(QLabel("交易数量"), 4, 0)
        grid.addWidget(QLabel("交易策略"), 5, 0)
        grid.addWidget(self.predict_at_first_time_checkbox, 0, 1, 1, 2)
        grid.addWidget(self.begin_datetime_edit, 1, 1, 1, 2)
        grid.addWidget(self.end_datetime_edit, 2, 1, 1, 2)
        grid.addWidget(self.refer_currency_combobox, 3, 1, 1, 2)
        grid.addWidget(self.trade_amount_edit, 4, 1, 1, 2)
        grid.addWidget(self.strategy_name_combobox,5,1,1,2)

        vbox_layout.addLayout(grid)

    def lock_all(self):
        self.predict_at_first_time_checkbox.setDisabled(True)
        self.begin_datetime_edit.setDisabled(True)
        self.end_datetime_edit.setDisabled(True)
        self.refer_currency_combobox.setDisabled(True)
        self.trade_amount_edit.setDisabled(True)
        self.strategy_name_combobox.setDisabled(True)

    def unlock_all(self):
        self.predict_at_first_time_checkbox.setEnabled(True)
        self.begin_datetime_edit.setEnabled(True)
        self.end_datetime_edit.setEnabled(True)
        self.refer_currency_combobox.setEnabled(True)
        self.trade_amount_edit.setEnabled(True)
        self.strategy_name_combobox.setEnabled(True)

    def get_setting_data(self) -> Any:
        predict_at_first_time = self.predict_at_first_time_checkbox.checkState() == Qt.CheckState.Unchecked
        begin_datetime = self.begin_datetime_edit.dateTime().toPyDateTime()
        end_datetime = self.end_datetime_edit.dateTime().toPyDateTime()
        refer_currency = self.refer_currency_combobox.currentText()
        trade_amount = float(self.trade_amount_edit.text())
        strategy_name = self.strategy_name_combobox.currentText()

        test_setting_data = TestSettingStruct(predict_at_first_time=predict_at_first_time, begin_datetime=begin_datetime, end_datetime=end_datetime, refer_currency=refer_currency, trade_amount=trade_amount, strategy_name=strategy_name)

        return test_setting_data
