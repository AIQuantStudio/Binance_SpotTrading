from PyQt6.QtCore import *
from PyQt6.QtWidgets import *
from PyQt6.QtGui import *

from market.binance_canvas import BinanceFigure



class ModelPanel(QFrame):
    
    def __init__(self, main_frame, app_engine):
        super().__init__(main_frame)

        self.setup_ui()
        
        
    def setup_ui(self):
        main_hbox_layout = QHBoxLayout()
        self.setLayout(main_hbox_layout)

        main_left_widget = QWidget()
        main_hbox_layout.addWidget(main_left_widget, stretch=3)

        main_right_widget = QWidget()
        main_hbox_layout.addWidget(main_right_widget, stretch=10)

        self.setup_left_area_ui(main_left_widget)
        self.setup_right_area_ui(main_right_widget)

    def setup_left_area_ui(self, left_widget):
        vbox_layout = QVBoxLayout()
        
        symbol_label = QLabel("交易对: ")
        vbox_layout.addWidget(symbol_label)
        
        config_info_label = QLabel("配置信息：")
        vbox_layout.addWidget(config_info_label)
        
        self.config_info_textbrowser = QTextBrowser()
        self.config_info_textbrowser.setFont(QFont('Courier New'))
        vbox_layout.addWidget(self.config_info_textbrowser)
        
        left_widget.setLayout(vbox_layout)
        
    def setup_right_area_ui(self, right_widget):
        vbox_layout = QVBoxLayout()
        right_widget.setLayout(vbox_layout)

        self.myfig=BinanceFigure()
        

        vbox_layout.addWidget(self.myfig)
        


        
        
        