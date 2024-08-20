from PyQt6.QtCore import *
from PyQt6.QtWidgets import *
from PyQt6.QtGui import *

from widget.trade_setting.trade_setting_interface import TradeSettingInterface
from model import ModelFactory


class TestTradeSettingPanel(QFrame, TradeSettingInterface):

    def __init__(self, parent_widget, top_dock):
        super().__init__(parent_widget)

        self.top_dock = top_dock
        
        self.setLineWidth(2)
        self.setMidLineWidth(2)
        self.setFrameStyle(QFrame.Shape.Panel | QFrame.Shadow.Sunken)

        vbox_layout = QVBoxLayout()
        self.setLayout(vbox_layout)

        self.predict_at_first_time = QCheckBox()
        self.predict_at_first_time.setToolTip("从启动时间开始预测")

        self.begin_datetime_edit = QDateTimeEdit()
        self.end_datetime_edit = QDateTimeEdit()

        self.refer_currency_combobox = QComboBox()
        self.refer_currency_combobox.addItems([currency for currency in ModelFactory().get_model_curreny(self.top_dock.id)])
        self.refer_currency_combobox.setItemDelegate(QStyledItemDelegate())

        double_validator = QDoubleValidator()
        double_validator.setBottom(0)
        self.trade_amount_edit = QLineEdit()
        self.trade_amount_edit.setValidator(double_validator)

        grid = QGridLayout()
        grid.addWidget(QLabel("从启动时间开始预测"), 0, 0)
        grid.addWidget(QLabel("起始时间"), 1, 0)
        grid.addWidget(QLabel("终止时间"), 2, 0)
        grid.addWidget(QLabel("交易对象"), 3, 0)
        grid.addWidget(QLabel("交易数量"), 4, 0)
        grid.addWidget(self.predict_at_first_time, 0, 1, 1, 2)
        grid.addWidget(self.begin_datetime_edit, 1, 1, 1, 2)
        grid.addWidget(self.end_datetime_edit, 2, 1, 1, 2)
        grid.addWidget(self.refer_currency_combobox, 3, 1, 1, 2)
        grid.addWidget(self.trade_amount_edit, 4, 1, 1, 2)

        vbox_layout.addLayout(grid)

    def lock_all(self):
        self.predict_at_first_time.setDisabled(True)
        self.begin_datetime_edit.setDisabled(True)
        self.end_datetime_edit.setDisabled(True)
        self.refer_currency_combobox.setDisabled(True)
        self.trade_amount_edit.setDisabled(True)

    def unlock_all(self):
        self.predict_at_first_time.setEnabled(True)
        self.begin_datetime_edit.setEnabled(True)
        self.end_datetime_edit.setEnabled(True)
        self.refer_currency_combobox.setEnabled(True)
        self.trade_amount_edit.setEnabled(True)

    def get_setting_data(self):
        data = {}
        data["Begin"] = self.begin_datetime_edit.dateTime().toMSecsSinceEpoch()
        data["End"] = self.end_datetime_edit.dateTime().toMSecsSinceEpoch()

        return data
