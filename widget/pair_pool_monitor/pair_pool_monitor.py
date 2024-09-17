from PyQt6.QtCore import *
from PyQt6.QtWidgets import *
from PyQt6.QtGui import *

from typing import List
from datetime import date, datetime, timedelta
import numpy as np
from sklearn.preprocessing import MinMaxScaler, StandardScaler

from widget.pair_pool_monitor.extended_combobox import ExtendedComboBox
from widget.pair_pool_monitor.relative_price_figure import RelativePriceFigure
from exchange import BinanceMarket
from common import Interval
from common import Utils


class PairPoolMonitor(QDialog):

    def __init__(self, parent_widget):
        super().__init__(parent_widget)

        self.setWindowTitle("相对价格监测")
        self.setMinimumWidth(1600)
        self.setMinimumHeight(900)

        self.all_symbol_list = []
        self.history_data: dict[str, list] = {}
        # self.interval_names = [i.value for i in Interval]

        self.setup_ui()
        self.load_all_symbol()

    def setup_ui(self):
        vbox_layout = QVBoxLayout()
        self.setLayout(vbox_layout)

        # 上半部分
        upper_hbox_layout = QHBoxLayout()

        self.setup_left_ui(upper_hbox_layout)
        self.setup_middle_ui(upper_hbox_layout)
        self.setup_right_ui(upper_hbox_layout)

        # 下半部分
        lower_hbox_layout = QHBoxLayout()

        self.figure = RelativePriceFigure()
        # widget.setMinimumHeight(200)

        lower_hbox_layout.addWidget(self.figure)

        vbox_layout.addLayout(upper_hbox_layout, stretch=2)
        vbox_layout.addLayout(lower_hbox_layout, stretch=3)

    def setup_left_ui(self, layout: QBoxLayout):
        self.all_symbol_combox = ExtendedComboBox()
        self.all_symbol_combox.addItems(self.all_symbol_list)
        self.all_symbol_combox.currentTextChanged.connect(self.all_symbol_combox_currentTextChanged)

        self.all_symbol_list_widget = QListWidget()
        self.all_symbol_list_widget.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)
        self.all_symbol_list_widget.addItems(self.all_symbol_list)
        self.all_symbol_list_widget.doubleClicked.connect(self.all_symbol_list_doubleClicked)

        vbox_layout_left = QVBoxLayout()
        vbox_layout_left.addWidget(self.all_symbol_combox)
        vbox_layout_left.addWidget(self.all_symbol_list_widget)

        add_btn = QPushButton("添加>>")
        add_btn.clicked.connect(self.add_btn_clicked)
        del_btn = QPushButton("<<删除")
        del_btn.clicked.connect(self.del_btn_clicked)
        clear_btn = QPushButton("清空")
        clear_btn.clicked.connect(self.clear_btn_clicked)

        vbox_layout_middle = QVBoxLayout()
        vbox_layout_middle.addStretch(1)
        vbox_layout_middle.addWidget(add_btn)
        vbox_layout_middle.addWidget(del_btn)
        vbox_layout_middle.addWidget(clear_btn)
        vbox_layout_middle.addStretch(1)

        self.right_list_widget = QListWidget()
        self.right_list_widget.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)
        # save_btn = QPushButton("保存")
        # save_btn.clicked.connect(self.save_btn_clicked)
        # load_btn = QPushButton("读取")
        # load_btn.clicked.connect(self.load_btn_clicked)
        
        vbox_layout_right = QVBoxLayout()
        vbox_layout_right.addWidget(self.right_list_widget)
        # vbox_layout_right.addWidget(save_btn)
        # vbox_layout_right.addWidget(load_btn)

        hbox_layout = QHBoxLayout()
        hbox_layout.addLayout(vbox_layout_left)
        hbox_layout.addLayout(vbox_layout_middle)
        hbox_layout.addLayout(vbox_layout_right)

        layout.addLayout(hbox_layout)

    def setup_middle_ui(self, layout: QBoxLayout):
        self.predict_at_first_time_checkbox = QCheckBox()
        self.predict_at_first_time_checkbox.setToolTip("从启动时间开始预测")

        self.begin_datetime_edit = QDateTimeEdit()
        self.begin_datetime_edit.setDateTime(QDateTime(datetime(2024, 1, 1)))
        self.end_datetime_edit = QDateTimeEdit()
        self.end_datetime_edit.setDateTime(QDateTime(datetime(2024, 1, 2)))

        self.interval_combobox = QComboBox()
        self.interval_combobox.addItems([i.value for i in Interval])
        # self.refer_currency_combobox.addItems([currency for currency in ModelFactory().get_model_curreny(self.app_id)])
        self.interval_combobox.setItemDelegate(QStyledItemDelegate())
        
        self.scaler_combobox = QComboBox()
        self.scaler_combobox.addItems([i.value for i in Scaler])
        # self.refer_currency_combobox.addItems([currency for currency in ModelFactory().get_model_curreny(self.app_id)])
        self.scaler_combobox.setItemDelegate(QStyledItemDelegate())

        self.start_btn = QPushButton("启动")
        self.start_btn.clicked.connect(self.start_btn_clicked)

        grid = QGridLayout()
        grid.addWidget(QLabel("起始时间"), 0, 0)
        grid.addWidget(QLabel("终止时间"), 1, 0)
        grid.addWidget(QLabel("间隔时间"), 2, 0)
        grid.addWidget(QLabel("规格模式"), 3, 0)
        grid.addWidget(self.begin_datetime_edit, 0, 1, 1, 2)
        grid.addWidget(self.end_datetime_edit, 1, 1, 1, 2)
        grid.addWidget(self.interval_combobox, 2, 1, 1, 2)
        grid.addWidget(self.scaler_combobox, 3, 1, 1, 2)
        grid.addWidget(self.start_btn, 4, 0, 1, 3)

        layout.addLayout(grid)

    def setup_right_ui(self, layout: QBoxLayout):
        self.log_info_textbrowser = QTextBrowser()
        self.log_info_textbrowser.setFont(QFont("Courier New", 11))
        # self.log_info_textbrowser.setMaximumHeight(200)
        layout.addWidget(self.log_info_textbrowser)

    def all_symbol_combox_currentTextChanged(self, cur_text: str):
        """下拉框选中"""
        total_count = self.all_symbol_list_widget.count()
        for i in range(total_count):
            item = self.all_symbol_list_widget.item(i)
            if item.text() == cur_text:
                item.setSelected(True)
                self.all_symbol_list_widget.setCurrentRow(i)
                break

    def check_submit_btn_clicked(self):
        """确认提交"""
        text_list = self.gain_right_all_list_text()
        if len(text_list) <= 0:
            QMessageBox.information(self, "提示", "您没有选择任何项", QMessageBox.StandardButton.Ok)
            return
        print(text_list)

    def all_symbol_list_doubleClicked(self, modelindex: QModelIndex):
        # self.close_edit()
        item = self.all_symbol_list_widget.item(modelindex.row())
        right_text_list = self.gain_right_all_list_text()
        if item.text() not in right_text_list:
            self.right_list_widget.addItem(item.text())
            
        self.cancel_left_list_selected()

    def add_btn_clicked(self):
        """从左侧添加项到右侧"""
        selected_items = self.all_symbol_list_widget.selectedItems()
        if len(selected_items) <= 0:
            QMessageBox.information(self, "提示", "请选择要添加的项", QMessageBox.StandardButton.Ok)
            return
        text_list = [i.text() for i in selected_items]
        right_text_list = self.gain_right_all_list_text()
        for item in text_list:
            if item in right_text_list:
                continue
            self.right_list_widget.addItem(item)
        self.cancel_left_list_selected()

    def gain_right_all_list_text(self) -> List[str]:
        """获取右侧列表中所有相的文本"""
        right_total_count = self.right_list_widget.count()
        text_list = []
        for i in range(right_total_count):
            item = self.right_list_widget.item(i)
            text_list.append(item.text())
        return text_list

    def del_btn_clicked(self):
        """从右侧将项删除"""
        selected_items = self.right_list_widget.selectedItems()
        if len(selected_items) <= 0:
            return
        for item in selected_items:
            # 拿出对象（凭借对象得到行数）以后移除
            self.right_list_widget.removeItemWidget(self.right_list_widget.takeItem(self.right_list_widget.row(item)))
        pass

    def all_selected_btn_clicked(self):
        """将左侧的项全部选中"""
        total_count = self.all_symbol_list_widget.count()
        for i in range(total_count):
            item = self.all_symbol_list_widget.item(i)
            item.setSelected(True)
        pass

    def cancel_seleced_btn_clicked(self):
        """取消左右两侧已选中的项"""
        self.cancel_left_list_selected()
        self.cancel_right_list_selected()
        pass

    def cancel_left_list_selected(self):
        selected_items = self.all_symbol_list_widget.selectedItems()
        if len(selected_items) <= 0:
            return
        for item in selected_items:
            item.setSelected(False)

    def cancel_right_list_selected(self):
        selected_items = self.right_list_widget.selectedItems()
        if len(selected_items) <= 0:
            return
        for item in selected_items:
            item.setSelected(False)

    def clear_btn_clicked(self):
        """清空右侧"""
        self.right_list_widget.clear()

    def load_all_symbol(self):
        with BinanceMarket() as market:
            self.all_symbol_list = market.get_all_symbol()

        self.all_symbol_combox.addItems(self.all_symbol_list)
        self.all_symbol_list_widget.addItems(self.all_symbol_list)

    def write_log(self, msg):
        self.log_info_textbrowser.append(msg)

    def start_btn_clicked(self):
        self.thread_a = QThread()
        self.thread_a.run = self.load_data
        self.thread_a.start()

        
        # self.load_data()
        # self.norm_data()
        # self.plot_data()

    def load_data(self):
        self.write_log("开始加载历史数据")

        begin_datetime = self.begin_datetime_edit.dateTime().toPyDateTime()
        end_datetime = self.end_datetime_edit.dateTime().toPyDateTime()

        if not end_datetime:
            end_datetime = datetime.now()

        if begin_datetime >= end_datetime:
            self.write_log("起始日期必须小于结束日期")
            return

        self.history_data.clear()

        # progress_delta = timedelta(hours=4)
        # interval_delta = timedelta(minutes=15)
        interval = Utils.convert_interval(self.interval_combobox.currentText())
        interval_delta = Utils.interval_to_timedelta(interval)
        progress_delta = 30 * interval_delta

        total_delta = end_datetime - begin_datetime
        start = begin_datetime
        end = begin_datetime + progress_delta
        progress = 0

        monitor_symbols = self.gain_right_all_list_text()
        
        with BinanceMarket() as market:
            while start < end_datetime:
                end = min(end, end_datetime)

                # data, data_end_time = load_bar_data(ModelFactory().get_model_symbol(self.model_id), start, end, interval_delta)
                data_end_time = 0
                for symbol in monitor_symbols:
                    data = market.load_klines(symbol, start, end, interval_delta)
                    if data_end_time < data[-1][0]:
                        data_end_time = data[-1][0]
                        
                    if symbol not in self.history_data:
                        self.history_data[symbol] = []
                        
                    self.history_data[symbol].extend(data)

                    # self._history_data.extend(data)

                progress += progress_delta / total_delta
                progress = min(progress, 1)
                progress_bar = "#" * int(progress * 10)
                self.write_log(f"加载进度：{progress_bar} [{progress:.0%}]")

                start = datetime.fromtimestamp(data_end_time / 1000.0) + interval_delta
                end += progress_delta + interval_delta

            self.write_log(f"历史数据加载完成，数据量：{len(self.history_data)}")

        self.norm_data()
        
    def norm_data(self):
        self.plot_data = []
        
        if Scaler.NORMALIZATION == Scaler(self.scaler_combobox.currentText()):
            scaler = MinMaxScaler()
        elif Scaler.STANDARDIZATION == Scaler(self.scaler_combobox.currentText()):
            scaler = StandardScaler()
        
        for symbol, data in self.history_data.items():
            
            # np_data = np.array(data)
            # norm_data = scaler.fit_transform(np_data)
            # price_data = norm_data[:,[4]].ravel()
            # print(price_data)
            
            np_data = np.array(data)
            
            timestamp_data = np_data[:,[0]]
            timestamp_data = timestamp_data.ravel()
            datetime_array = Utils.timestamp_array_to_datetime_array(timestamp_data.tolist())
            x = np.array(datetime_array)
            
            
            price_data = np_data[:,[4]]
            norm_data = scaler.fit_transform(price_data)
            y = norm_data.ravel()
            
            plot = {
                "name":symbol,
                "x": x,
                "y": y
            }
            self.plot_data.append(plot)
        
        self.figure.plot_multi_line(self.plot_data)
            