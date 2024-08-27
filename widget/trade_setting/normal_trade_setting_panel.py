from PyQt6.QtCore import *
from PyQt6.QtWidgets import *
from PyQt6.QtGui import *

from widget.trade_setting.trade_setting_interface import TradeSettingInterface

    
class NormalTradeSettingPanel(QFrame, TradeSettingInterface):

    def __init__(self, parent_widget, app_id):
        super().__init__(parent_widget)

        self.app_id = app_id
        
        self.setLineWidth(2)
        self.setMidLineWidth(2)
        self.setFrameStyle(QFrame.Shape.Panel | QFrame.Shadow.Sunken)
        
        vbox_layout = QVBoxLayout()
        self.setLayout(vbox_layout)

        exchanges = ["A", "B", "C"]
        self.exchange_combo = QComboBox()
        self.exchange_combo.addItems([exchange for exchange in exchanges])
        self.exchange_combo.setItemDelegate(QStyledItemDelegate())
        
        self.symbol_line = QDateTimeEdit()
        # self.symbol_line.returnPressed.connect(self.set_vt_symbol)

        self.name_line = QLineEdit()
        self.name_line.setReadOnly(True)
        

        self.offset_combo = QComboBox()
        # self.offset_combo.addItems([offset.value for offset in Offset])
        self.offset_combo.setItemDelegate(QStyledItemDelegate())

        self.order_type_combo = QComboBox()
        # self.order_type_combo.addItems([order_type.value for order_type in OrderType])
        self.order_type_combo.setItemDelegate(QStyledItemDelegate())

        double_validator = QDoubleValidator()
        double_validator.setBottom(0)

        self.price_line = QLineEdit()
        self.price_line.setValidator(double_validator)

        self.volume_line = QLineEdit()
        self.volume_line.setValidator(double_validator)

        self.gateway_combo = QComboBox()
        self.gateway_combo.addItems(["AAA", "BBBB"])
        self.gateway_combo.setItemDelegate(QStyledItemDelegate())


        self.direction_combo = QComboBox()
        self.direction_combo.addItems(["买", "卖"])
        self.direction_combo.setItemDelegate(QStyledItemDelegate())
        
        self.price_check = QCheckBox()
        self.price_check.setToolTip("设置价格随行情更新")

        send_button = QPushButton("委托")
        # send_button.clicked.connect(self.send_order)

        cancel_button = QPushButton("全撤")
        # cancel_button.clicked.connect(self.cancel_all)
        
        # self.table = QTableWidget(4,3,self)
        # self.table.setHorizontalHeaderLabels(['第一列', '第二列', '第三列'])
        grid = QGridLayout()
        grid.addWidget(QLabel("交易所"), 0, 0)
        grid.addWidget(QLabel("代码"), 1, 0)
        grid.addWidget(QLabel("名称"), 2, 0)
        grid.addWidget(QLabel("方向"), 3, 0)
        grid.addWidget(QLabel("开平"), 4, 0)
        grid.addWidget(QLabel("类型"), 5, 0)
        grid.addWidget(QLabel("价格"), 6, 0)
        grid.addWidget(QLabel("数量"), 7, 0)
        grid.addWidget(QLabel("接口"), 8, 0)
        grid.addWidget(self.exchange_combo, 0, 1, 1, 2)
        grid.addWidget(self.symbol_line, 1, 1, 1, 2)
        grid.addWidget(self.name_line, 2, 1, 1, 2)
        grid.addWidget(self.direction_combo, 3, 1, 1, 2)
        grid.addWidget(self.offset_combo, 4, 1, 1, 2)
        grid.addWidget(self.order_type_combo, 5, 1, 1, 2)
        grid.addWidget(self.price_line, 6, 1, 1, 1)
        grid.addWidget(self.price_check, 6, 2, 1, 1)
        grid.addWidget(self.volume_line, 7, 1, 1, 2)
        grid.addWidget(self.gateway_combo, 8, 1, 1, 2)

        vbox_layout.addLayout(grid)

    def lock_all_input(self):
        pass
    
    def unlock_all_input(self):
        pass
    
    def get_setting_data(self):
        pass