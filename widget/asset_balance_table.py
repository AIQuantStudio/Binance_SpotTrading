from PyQt6.QtCore import *
from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
from typing import Dict

from structure import AssetBalanceData
from event import Event, EVENT_ASSET_BALANCE
from main_engine import MainEngine

from widget.asset_balance_cells.asset_balance_str_cell import AssetBalanceStrCell
from widget.asset_balance_cells.asset_balance_float_cell import AssetBalanceFloatCell


class AssetBalanceTable(QTableWidget):

    signal_refresh_asset_balance: pyqtSignal = pyqtSignal(Event)
    
    record_key = "currency"
    headers: Dict[str, dict] = {
        "currency": {"display": "账号", "type": AssetBalanceStrCell, "width_factor": 2},
        "total": {"display": "余额", "type": AssetBalanceFloatCell,  "width_factor": 4},
        "locked": {"display": "冻结", "type": AssetBalanceFloatCell,  "width_factor": 4},
        "free": {"display": "可用", "type": AssetBalanceFloatCell,  "width_factor": 4},
    }
    
    def __init__(self, parent_widget, app_id):
        super().__init__(parent_widget)
        
        self.app_id = app_id

        self.record_cells: Dict[str, dict] = {}
        self.record_tables: Dict[str, QTableWidget] = {}
        self._first_painted = False
        
        self.init_ui()
        # self.register_event()
        
        self.signal_refresh_asset_balance.connect(self.process_refresh_asset_balance_event)
        MainEngine.event_engine.register(EVENT_ASSET_BALANCE, self.signal_refresh_asset_balance.emit)
    
    def event(self, event: QEvent) -> bool:
        """ 重写 QTableWidget::event 用于设定列宽 """
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
        # 将表格变为禁止编辑
        self.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.setAlternatingRowColors(True)
        self.setSortingEnabled(True)

    
    def process_refresh_asset_balance_event(self, event):
        self.setSortingEnabled(False)

        balance_data: AssetBalanceData = event.data
        
        record_key = balance_data.__getattribute__(self.record_key)
        if record_key in self.record_cells:
            self._update_row(balance_data)
        else:
            self._insert_record(balance_data)

        self.setSortingEnabled(True)
    
    def _insert_record(self, data: AssetBalanceData):
        self.insertRow(0)

        row_cells = {}
        for column, header in enumerate(self.headers.keys()):
            content = data.__getattribute__(header)
            cell = self.headers[header]["type"](content)
            self.setItem(0, column, cell)
            row_cells[header] = cell

        record_key = data.__getattribute__(self.record_key)
        self.record_cells[record_key] = row_cells

    def _update_row(self, data: AssetBalanceData):
        record_key = data.__getattribute__(self.record_key)
        record = self.record_cells[record_key]

        for header, cell in record.items():
            content = data.__getattribute__(header)
            cell.set_content(content)


    def clear_contents(self):
        rows = self.rowCount()
        self.record_cells = {}
        for row in range(rows - 1, -1, -1):
            self.removeRow(row)
    
    def close(self):
        MainEngine.event_engine.unregister(EVENT_ASSET_BALANCE, self.signal_refresh_asset_balance.emit)
        return super().close()