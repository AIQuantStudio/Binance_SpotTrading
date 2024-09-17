from PyQt6.QtCore import *
from PyQt6.QtWidgets import *
from PyQt6.QtGui import *

from typing import Dict
from event import Event
from event import EVENT_TRADE
from main_engine import MainEngine
# from common import TradeData

from widget.trade_history_cells.trade_history_str_cell import TradeHistoryStrCell
from widget.trade_history_cells.trade_history_float_cell import TradeHistoryFloatCell
from widget.trade_history_cells.trade_history_time_cell import TradeHistoryTimeCell
from widget.trade_history_cells.trade_history_enum_cell import TradeHistoryEnumCell
from widget.trade_history_cells.trade_history_direction_cell import TradeHistoryDirectionCell


class TradeHistoryMonitor(QTableWidget):
    
    signal: pyqtSignal = pyqtSignal(Event)
    headers: Dict[str, dict] = {
        "trade_id": {"display": "成交号 ", "type": TradeHistoryStrCell, "width_factor": 1},
        "order_id": {"display": "委托号", "type": TradeHistoryStrCell, "width_factor": 1},
        "symbol": {"display": "代码", "type": TradeHistoryStrCell, "width_factor": 1},
        "exchange": {"display": "交易所", "type": TradeHistoryEnumCell, "width_factor": 1},
        "direction": {"display": "方向", "type": TradeHistoryDirectionCell, "width_factor": 1},
        "offset": {"display": "开平", "type": TradeHistoryEnumCell, "width_factor": 1},
        "price": {"display": "价格", "type": TradeHistoryFloatCell, "width_factor": 1},
        "volume": {"display": "数量", "type": TradeHistoryFloatCell, "width_factor": 1},
        "datetime": {"display": "时间", "type": TradeHistoryTimeCell, "width_factor": 1},
        "gateway_name": {"display": "接口", "type": TradeHistoryStrCell, "width_factor": 1},
    }

    def __init__(self, parent_widget, app_id):
        super().__init__(parent_widget)

        self.app_id = app_id

        self._first_painted = False

        self.init_ui()
        self.register_event()

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

    def init_ui(self) -> None:
        hearder_labels = [d["display"] for d in self.headers.values()]

        self.setColumnCount(len(hearder_labels))
        self.setHorizontalHeaderLabels(hearder_labels)
        self.verticalHeader().setVisible(False)
        # self.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.setAlternatingRowColors(True)
        self.setSortingEnabled(True)

    def register_event(self) -> None:
        self.signal.connect(self.process_event)
        MainEngine.event_engine.register(EVENT_TRADE, self.signal.emit)

    def process_event(self, event: Event) -> None:
        self.setSortingEnabled(False)

        trade_data: TradeData = event.data
        self._insert_record(trade_data)

        self.setSortingEnabled(True)

    def _insert_record(self, data):
        self.insertRow(0)
        for column, header in enumerate(self.headers.keys()):
            content = data.__getattribute__(header)
            cell = self.headers[header]["type"](content)
            self.setItem(0, column, cell)
