from PyQt6.QtCore import *
from PyQt6.QtWidgets import *
from PyQt6.QtGui import *

from main_engine import MainEngine
from event import Event, EVENT_LOG
from structure import LogStruct
from widget.log_monitor_cells.log_msg_cell import LogMsgCell
from widget.log_monitor_cells.log_time_cell import LogTimeCell


class LogMonitor(QTableWidget):

    signal: pyqtSignal = pyqtSignal(Event)
    headers = {
        "time": {"display": "时间", "type": LogTimeCell, "width_factor": 3},
        "msg": {"display": "信息", "type": LogMsgCell, "width_factor": 7},
    }

    def __init__(self, parent_widget, app_id):
        super().__init__(parent_widget)

        self.app_id = app_id
        self._first_painted = False

        self.init_ui()
        self.register_event()

    def event(self, event: QEvent) -> bool:
        """重写 QTableWidget::event"""
        if event.type() == QEvent.Type.Paint:
            if not self._first_painted:
                width_factors = [d["width_factor"] for d in self.headers.values()]
                width_sum = sum(width_factors)
                width = self.viewport().width() / width_sum
                for i, factor in enumerate(width_factors):
                    self.setColumnWidth(i, int(width * factor))

                self._first_painted = True

        return super().event(event)

    def init_ui(self):
        hearder_labels = [d["display"] for d in self.headers.values()]
        self.setColumnCount(len(hearder_labels))
        self.setHorizontalHeaderLabels(hearder_labels)
        self.verticalHeader().setVisible(False)
        self.setEditTriggers(self.EditTrigger.NoEditTriggers)
        self.setAlternatingRowColors(True)
        self.setSortingEnabled(False)

    def register_event(self):
        self.signal.connect(self.process_event)
        MainEngine.event_engine.register(EVENT_LOG, self.signal.emit, suffix=self.app_id)

    def process_event(self, event: Event):
        log_data: LogStruct = event.data
        self.insert_record(log_data)

    def insert_record(self, data: LogStruct):
        self.insertRow(0)
        for column, header in enumerate(self.headers.keys()):
            content = data.__getattribute__(header)
            cell = self.headers[header]["type"](content)
            self.setItem(0, column, cell)

    def close(self) -> bool:
        self.signal.disconnect(self.process_event)
        MainEngine.event_engine.unregister(EVENT_LOG, self.signal.emit, suffix=self.app_id)

        return super().close()
