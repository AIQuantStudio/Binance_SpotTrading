from PyQt6.QtCore import *
from PyQt6.QtWidgets import *
from PyQt6.QtGui import *

from typing import List
from datetime import datetime
import numpy as np

from widget.pair_pool_monitor.extended_combobox import ExtendedComboBox
from exchange import BinanceMarket


class PairPoolMonitor(QDialog):

    def __init__(self, parent_widget):
        super().__init__(parent_widget)

        self.setWindowTitle("相对价格监测")
        self.setMinimumWidth(1600)
        self.setMinimumHeight(900)

        self.all_symbol_list = []

        self.init_ui()
        self.load_all_symbol()

    def init_ui(self):
        vbox_layout = QVBoxLayout()
        self.setLayout(vbox_layout)

        #上半部分
        upper_hbox_layout = QHBoxLayout()

        self.setup_left_ui(upper_hbox_layout)
        self.setup_middle_ui(upper_hbox_layout)
        self.setup_right_ui(upper_hbox_layout)

        #下半部分
        lower_hbox_layout = QHBoxLayout()
        
        widget = QFrame()
        # widget.setMinimumHeight(200)
        
        lower_hbox_layout.addWidget(widget)

        
        vbox_layout.addLayout(upper_hbox_layout, stretch=2)
        vbox_layout.addLayout(lower_hbox_layout, stretch=3)
        
    def setup_left_ui(self, layout: QBoxLayout):
        self.all_symbol_combox = ExtendedComboBox()
        self.all_symbol_combox.addItems(self.all_symbol_list)
        self.all_symbol_combox.currentTextChanged.connect(self.combox_currentTextChanged)

        self.left_list_widget = QListWidget()
        self.left_list_widget.setSelectionMode(QAbstractItemView.SelectionMode.MultiSelection)
        self.left_list_widget.addItems(self.all_symbol_list)

        layout_1 = QVBoxLayout()
        layout_1.addWidget(self.all_symbol_combox)
        layout_1.addWidget(self.left_list_widget)

        add_btn = QPushButton("添加>>")
        add_btn.clicked.connect(self.add_btn_clicked)
        del_btn = QPushButton("<<删除")
        del_btn.clicked.connect(self.del_btn_clicked)
        clear_btn = QPushButton("清空")
        clear_btn.clicked.connect(self.clear_btn_clicked)

        layout_2 = QVBoxLayout()
        layout_2.addStretch(1)
        layout_2.addWidget(add_btn)
        layout_2.addWidget(del_btn)
        layout_2.addWidget(clear_btn)
        layout_2.addStretch(1)

        self.right_list_widget = QListWidget()
        self.right_list_widget.setSelectionMode(QAbstractItemView.SelectionMode.MultiSelection)

        layout_3 = QHBoxLayout()
        layout_3.addLayout(layout_1)
        layout_3.addLayout(layout_2)
        layout_3.addWidget(self.right_list_widget)

        layout.addLayout(layout_3)

    def setup_middle_ui(self, layout:QBoxLayout):
        self.predict_at_first_time_checkbox = QCheckBox()
        self.predict_at_first_time_checkbox.setToolTip("从启动时间开始预测")

        self.begin_datetime_edit = QDateTimeEdit()
        self.begin_datetime_edit.setDateTime(QDateTime(datetime(2024, 1, 1)))
        self.end_datetime_edit = QDateTimeEdit()
        self.end_datetime_edit.setDateTime(QDateTime(datetime(2024, 1, 2)))

        self.refer_currency_combobox = QComboBox()
        # self.refer_currency_combobox.addItems([currency for currency in ModelFactory().get_model_curreny(self.app_id)])
        self.refer_currency_combobox.setItemDelegate(QStyledItemDelegate())

        self.start_btn = QPushButton("启动")
        # self.start_btn.clicked.connect(self.add_btn_clicked)

        grid = QGridLayout()
        grid.addWidget(QLabel("从启动时间开始预测"), 0, 0)
        grid.addWidget(QLabel("起始时间"), 1, 0)
        grid.addWidget(QLabel("终止时间"), 2, 0)
        grid.addWidget(QLabel("交易对象"), 3, 0)
        grid.addWidget(QLabel("交易数量"), 4, 0)
        grid.addWidget(self.predict_at_first_time_checkbox, 0, 1, 1, 2)
        grid.addWidget(self.begin_datetime_edit, 1, 1, 1, 2)
        grid.addWidget(self.end_datetime_edit, 2, 1, 1, 2)
        grid.addWidget(self.refer_currency_combobox, 3, 1, 1, 2)
        grid.addWidget(self.start_btn, 4, 1, 1, 2)

        layout.addLayout(grid)

    def setup_right_ui(self, layout: QBoxLayout):
        self.config_info_textbrowser = QTextBrowser()
        self.config_info_textbrowser.setFont(QFont("Courier New", 11))
        self.config_info_textbrowser.setMaximumHeight(200)
        layout.addWidget(self.config_info_textbrowser)

    def combox_currentTextChanged(self, cur_text: str):
        """下拉框选中"""
        total_count = self.left_list_widget.count()
        for i in range(total_count):
            item = self.left_list_widget.item(i)
            if item.text() == cur_text:
                item.setSelected(True)
                self.left_list_widget.setCurrentRow(i)
                break
        pass

    def check_submit_btn_clicked(self):
        """确认提交"""
        text_list = self.gain_right_all_list_text()
        if len(text_list) <= 0:
            QMessageBox.information(self, "提示", "您没有选择任何项", QMessageBox.StandardButton.Ok)
            return
        print(text_list)
        pass

    def add_btn_clicked(self):
        """从左侧添加项到右侧"""
        selected_items = self.left_list_widget.selectedItems()
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
        pass

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
        total_count = self.left_list_widget.count()
        for i in range(total_count):
            item = self.left_list_widget.item(i)
            item.setSelected(True)
        pass

    def cancel_seleced_btn_clicked(self):
        """取消左右两侧已选中的项"""
        self.cancel_left_list_selected()
        self.cancel_right_list_selected()
        pass

    def cancel_left_list_selected(self):
        selected_items = self.left_list_widget.selectedItems()
        if len(selected_items) <= 0:
            return
        for item in selected_items:
            item.setSelected(False)
        pass

    def cancel_right_list_selected(self):
        selected_items = self.right_list_widget.selectedItems()
        if len(selected_items) <= 0:
            return
        for item in selected_items:
            item.setSelected(False)
        pass

    def clear_btn_clicked(self):
        """清空右侧"""
        self.right_list_widget.clear()
        pass

    def load_all_symbol(self):
        with BinanceMarket() as market:
            self.all_symbol_list = market.get_all_symbol()
            
        self.all_symbol_combox.addItems(self.all_symbol_list)
        self.left_list_widget.addItems(self.all_symbol_list)

        