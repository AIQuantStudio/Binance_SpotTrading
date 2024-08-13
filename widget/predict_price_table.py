from PyQt6.QtCore import *
from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
from typing import Dict

from widget.predict_price_cells.predict_price_time_cell import PrdictPriceTimeCell
from widget.predict_price_cells.predict_price_float_cell import PredictPriceFloatCell
from widget.predict_price_cells.predict_price_trend_cell import PredictPriceTrendCell
from event import Event, EVENT_ASSET_BALANCE
from structure.asset_balance_data import AssetBalanceData


class PredictPriceTable(QTableWidget):

        
    signal_refresh_asset_balance: pyqtSignal = pyqtSignal(Event)
    
    record_key = "symbol"
    headers: Dict[str, dict] = {
        "time": {"display": "时间", "type": PrdictPriceTimeCell, "width_factor": 4},
        "price": {"display": "价格", "type": PredictPriceFloatCell,  "width_factor": 4},
        "trend": {"display": "涨跌", "type": PredictPriceTrendCell,  "width_factor": 2},
    }
    
    def __init__(self, parent_widget, top_dock, app_engine):
        """"""
        super().__init__(parent_widget)
        
        self.top_dock = top_dock
        self.app_engine = app_engine

        self.record_cells: Dict[str, dict] = {} # 记录返回数据
        self.record_tables: Dict[str, QTableWidget] = {} # 记录表格
        self._first_painted = False
        
        self.init_ui()
        # self.register_event()
        # self.create_asset_balance_table()
    
    def event(self, event: QEvent) -> bool:
        """ 重写 QTableWidget::event """
        if event.type() == QEvent.Paint:
            if not self._first_painted:
                width_factors = [d["width_factor"] for d in self.headers.values()]
                width_sum = sum(width_factors)
                width = self.viewport().width()/width_sum
                for i, factor in enumerate(width_factors):
                    self.setColumnWidth(i, int(width * factor))

                self._first_painted = True

        return super().event(event)
    
    def init_ui(self):
        hearder_labels = [d["display"] for d in self.headers.values()]

        self.setColumnCount(len(hearder_labels))
        self.setHorizontalHeaderLabels(hearder_labels)
        self.verticalHeader().setVisible(False)
        self.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.setAlternatingRowColors(True)
        self.setSortingEnabled(True)
        
        # self.balances_table = None
        # self.setCurrentIndex(0)
        
    # def register_event(self) -> None:
    #     self.signal_refresh_asset_balance.connect(self.process_event)
    #     self.app_engine.event_engine.register(EVENT_ASSET_BALANCE, self.signal_refresh_asset_balance.emit)
        
    def create_asset_balance_table(self):
        table = QTableWidget()
        hearder_labels = [d["display"] for d in self.headers.values()]
        table.setColumnCount(len(hearder_labels))
        table.setHorizontalHeaderLabels(hearder_labels)
        # 表格头的显示与隐藏
        #垂直方向
        table.verticalHeader().setVisible(False)
        # 将表格变为禁止编辑
        table.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        table.setAlternatingRowColors(True)
        table.setSortingEnabled(True)
        # 设置表格头为伸缩模式
        # accTable.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)

        return table
    
    def process_event(self, event) -> None:
        self.setSortingEnabled(False)
        
        # self.setSortingEnabled(False)
        # 获取返回的数据
        balance_data: AssetBalanceData = event.data
        print(balance_data)
        
        # 获取数据的key
        record_key = balance_data.__getattribute__(self.record_key)
        print(record_key)
        # 判断数据是否存在
        if record_key in self.record_cells:
            self._update_row(balance_data)
        else:
            self._insert_record(balance_data)

        self.setSortingEnabled(True)
    
    def _insert_record(self, data: AssetBalanceData):
        """"""
        self.insertRow(0)

        row_cells = {}
        for column, header in enumerate(self.headers.keys()):
            content = data.__getattribute__(header)
            cell = self.headers[header]["type"](content)
            self.setItem(0, column, cell)
            row_cells[header] = cell

        record_key = data.__getattribute__(self.record_key)
        self.record_cells[record_key] = row_cells
        print("-----")
        print(self.record_cells)

    def _update_row(self, data: AssetBalanceData) -> None:
        """"""
        record_key = data.__getattribute__(self.record_key)
        record = self.record_cells[record_key]

        for header, cell in record.items():
            content = data.__getattribute__(header)
            cell.set_content(content)


    def clear_table(self):
        # 获取表格的行数和列数
        rows = self.rowCount()
        
        columns = self.columnCount()
    
        # 从最后一行开始反向遍历，以便于删除行时不影响循环
        self.record_cells = {}
        for row in range(rows - 1, -1, -1):
            self.removeRow(row)
    
