from PyQt6.QtCore import *
from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
from typing import Dict

from frame.asset_balance_cells.asset_balance_str_cell import AssetBalanceStrCell
from frame.asset_balance_cells.asset_balance_float_cell import AssetBalanceFloatCell
from event import Event, EVENT_ASSET_BALANCE
from structure.asset_balance_data import AssetBalanceData


class AssetBalancePenal(QToolBox):

    # def __init__(self, parent_widget, top_dock, app_engine):
    #     super().__init__(parent_widget)

    #     self.top_dock = top_dock
    #     self.app_engine = app_engine

    #     self.setup_ui()

    # def setup_ui(self):
    #     vbox_layout = QVBoxLayout()
    #     self.setLayout(vbox_layout)

    #     self.table = QTableWidget(4,3,self)
    #     self.table.setHorizontalHeaderLabels(['第一列', '第二列', '第三列'])

    #     vbox_layout.addWidget(self.table)
        
    signal_refresh_asset_balance: pyqtSignal = pyqtSignal(Event)
    
    headers: Dict[str, dict] = {
        "account_id": {"display": "账号", "type": AssetBalanceStrCell, "width_factor": 3},
        "balance": {"display": "余额", "type": AssetBalanceFloatCell,  "width_factor": 2},
        "frozen": {"display": "冻结", "type": AssetBalanceFloatCell,  "width_factor": 2},
        "available": {"display": "可用", "type": AssetBalanceFloatCell,  "width_factor": 2},
        "gateway_name": {"display": "接口", "type": AssetBalanceStrCell,  "width_factor": 2},
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
        self.register_event()

    def init_ui(self):
        self.setCurrentIndex(0)
        
    def register_event(self) -> None:
        self.signal_refresh_asset_balance.connect(self.process_event)
        self.app_engine.event_engine.register(EVENT_ASSET_BALANCE, self.signal_refresh_asset_balance.emit)
        
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
        """监听事件触发方法"""
        # self.setSortingEnabled(False)
        # 获取返回的数据
        account_data: AssetBalanceData = event.data
        print(account_data)
        
        # 判断当前门户是否已生成表格
        gatTable: QTableWidget = None
        if gateway_name not in self.record_tables:
            # 生成表格
            gatTable = self.create_trade_table()
            # 门户信息保存对应json文件名
            settingFileName: str = f"connect_{gateway_name.lower()}.json"
            # 获取当前门户保存的属性信息
            settingData = Setting.load_setting_json(settingFileName)
            # 获取用户名
            # accountName = settingData['name']
            accountName = settingData['activeGateway']
            # 添加表格到折叠框中
            self.addItem(gatTable, gateway_name + '-' + accountName)
            self.record_tables[gateway_name] = gatTable
            # 按比例设置单元格宽度
            width_factors = [d["width_factor"] for d in self.headers.values()]
            width_sum = sum(width_factors)
            width = gatTable.viewport().width()/width_sum
            for i, factor in enumerate(width_factors):
                gatTable.setColumnWidth(i, width * factor)
        else:
            gatTable = self.record_tables[gateway_name]

        # 获取数据的key
        record_key = account_data.__getattribute__(self.record_key)
        # 判断数据是否存在
        if record_key in self.record_cells:
            self._update_row(account_data, gatTable)
        else:
            self._insert_record(account_data, gatTable)

        # self.setSortingEnabled(True)
    
    def _insert_record(self, data: AssetBalanceData, gatTable: QTableWidget):
        """"""
        gatTable.insertRow(0)

        row_cells = {}
        for column, header in enumerate(self.headers.keys()):
            content = data.__getattribute__(header)
            cell = self.headers[header]["type"](content)
            gatTable.setItem(0, column, cell)
            row_cells[header] = cell

        record_key = data.__getattribute__(self.record_key)
        self.record_cells[record_key] = row_cells

    def _update_row(self, data: AssetBalanceData, gatTable: QTableWidget) -> None:
        """"""
        record_key = data.__getattribute__(self.record_key)
        record = self.record_cells[record_key]

        for header, cell in record.items():
            content = data.__getattribute__(header)
            cell.set_content(content)

