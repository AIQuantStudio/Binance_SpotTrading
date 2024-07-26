from PyQt6.QtCore import *
from PyQt6.QtWidgets import *
from PyQt6.QtGui import *

class MainFrame(QFrame):
    
    def __init__(self, parent_widget, app_engine):
        super().__init__(parent_widget)
        
        self.setFrameStyle(QFrame.Shape.Box | QFrame.Shadow.Sunken)
        self.setLineWidth(1)
        self.setMidLineWidth(1)
        
        lay = QVBoxLayout(self)
        lay.setContentsMargins(10, 10, 10, 10)
        
        
        # main_widget = QWidget()
        panel_vbox_layout = QVBoxLayout()
        self.setLayout(panel_vbox_layout)

        main_top_widget = QWidget()
        panel_vbox_layout.addWidget(main_top_widget, stretch=2)

        main_bottom_widget = QWidget()
        panel_vbox_layout.addWidget(main_bottom_widget, stretch=10)

        self.setup_left_area_ui(main_top_widget)
        self.setup_right_area_ui(main_bottom_widget)

        self.setLayout(main_widget)
        
        
        
        
        
        # self.select_account_btn = QPushButton("选择账号")
        # self.select_account_btn.setFixedHeight(30)
        # self.select_account_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        # self.select_account_btn.setStyleSheet("QPushButton:hover { color: #333; }")
        # self.select_account_btn.setFixedWidth(100)
        # lay.addWidget(self.select_account_btn)
        
    def setup_left_area_ui(self, base_widget):
        vbox_layout = QVBoxLayout()

        model_frame = QFrame(self)
        model_frame.setFrameShape(QFrame.Shape.StyledPanel)
        binance_frame = QFrame(self)
        binance_frame.setFrameShape(QFrame.Shape.StyledPanel)
        
        model_vbox_layout = QVBoxLayout()
        binance_vbox_layout = QVBoxLayout()
        model_frame.setLayout(model_vbox_layout)
        binance_frame.setLayout(binance_vbox_layout)
        
        
        self.line = QFrame(self)
        self.line.setGeometry(QRect(0, 120, 341, 20))
        self.line.setFrameShadow(QFrame.Shadow.Sunken)
        self.line.setLineWidth(5)
        self.line.setFrameShape(QFrame.Shape.HLine)

        splitter = QSplitter(Qt.Orientation.Vertical)
        splitter.addWidget(model_frame)
        splitter.addWidget(self.line)
        splitter.addWidget(binance_frame)
        vbox_layout.addWidget(splitter)
        
        first_hbox_layout = QHBoxLayout()
        # 载入模型按钮
        self.loading_model_btn = QPushButton("选择模型")
        self.loading_model_btn.setFixedHeight(30)
        self.loading_model_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.loading_model_btn.setStyleSheet("QPushButton:hover { color: #333; }")
        # self.loading_model_btn.setStyleSheet(css_loading_model_on)
        self.loading_model_btn.setFixedWidth(100)
        first_hbox_layout.addWidget(self.loading_model_btn)
        # 模型名称标签
        self.model_name_label = QLabel("")
        first_hbox_layout.addWidget(self.model_name_label)
        model_vbox_layout.addLayout(first_hbox_layout)
    
        # 加载参数按钮
        self.loading_parameters_btn = QPushButton("加载参数")
        self.loading_parameters_btn.setFixedHeight(30)
        self.loading_parameters_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        # self.loading_parameters_btn.setStyleSheet(css_loading_model_on)
        self.loading_parameters_btn.setFixedWidth(100)
        self.loading_parameters_btn.setDisabled(True)
        model_vbox_layout.addWidget(self.loading_parameters_btn)
        
        # 交易对 GPU
        second_hbox_layout = QHBoxLayout()
        second_left_widget = QWidget()
        second_hbox_layout.addWidget(second_left_widget, stretch=8)
        second_right_widget = QWidget()
        second_hbox_layout.addWidget(second_right_widget, stretch=3)
        
        second_left_hbox_layout = QHBoxLayout()
        pair_name_label = QLabel("交易对: ")
        second_left_hbox_layout.addWidget(pair_name_label)
        self.pair_name_LineEdit = QLineEdit()
        self.pair_name_LineEdit.setEnabled(False)
        second_left_hbox_layout.addWidget(self.pair_name_LineEdit)
        second_left_widget.setLayout(second_left_hbox_layout)
        
        second_right_hbox_layout = QHBoxLayout()
        self.is_gpu_checkbox = QCheckBox("GPU")
        self.is_gpu_checkbox.setDisabled(True)
        second_right_hbox_layout.addWidget(self.is_gpu_checkbox)
        second_right_widget.setLayout(second_right_hbox_layout)
        
        model_vbox_layout.addLayout(second_hbox_layout)
        
        
        # 配置信息
        config_info_label = QLabel("配置信息：")
        model_vbox_layout.addWidget(config_info_label)
        self.config_info_textbrowser = QTextBrowser()
        self.config_info_textbrowser.setFont(QFont('Courier New'))
        model_vbox_layout.addWidget(self.config_info_textbrowser)
        
        ##################################################
        
        
        binance_first_hbox_layout = QHBoxLayout()
        # 选择账号
        self.select_account_btn = QPushButton("选择账号")
        self.select_account_btn.setFixedHeight(30)
        self.select_account_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.select_account_btn.setStyleSheet("QPushButton:hover { color: #333; }")
        # self.loading_model_btn.setStyleSheet(css_loading_model_on)
        self.select_account_btn.setFixedWidth(100)
        binance_first_hbox_layout.addWidget(self.select_account_btn)
        # 模型名称标签
        self.account_name_label = QLabel("")
        binance_first_hbox_layout.addWidget(self.account_name_label)
        binance_vbox_layout.addLayout(binance_first_hbox_layout)
        

        # 开始按钮
        self.btn_switch = QPushButton("开始监控")
        self.btn_switch.setFixedHeight(30)
        self.btn_switch.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_switch.setStyleSheet(";".join(switch_on_css_list))
        binance_vbox_layout.addWidget(self.btn_switch)

        # 下注上限
        h_box_Layout = QHBoxLayout()
        lbl_name = QLabel("下注上限")
        h_box_Layout.addWidget(lbl_name, 3)
        self.maxBetVal = QLineEdit("1")
        h_box_Layout.addWidget(self.maxBetVal, 9)
        binance_vbox_layout.addLayout(h_box_Layout)

        # 日志
        lbl_output_log = QLabel("日志：")
        binance_vbox_layout.addWidget(lbl_output_log)
        self.txtbrowser_output_log = QTextBrowser()
        binance_vbox_layout.addWidget(self.txtbrowser_output_log)

        widget.setLayout(vbox_layout)