from PyQt6.QtCore import *
from PyQt6.QtWidgets import *
from PyQt6.QtGui import *

class MainFrame(QFrame):
    
    def __init__(self, parent_widget, app_engine):
        super().__init__(parent_widget)
        
        self.setLineWidth(1)
        self.setMidLineWidth(1)
        self.setFrameStyle(QFrame.Shape.Box | QFrame.Shadow.Sunken)
        # self.setFixedWidth(800)
        # self.setup_ui()
        
        
        lay = QVBoxLayout(self)
        lay.setContentsMargins(10, 10, 10, 10)
        self.select_account_btn = QPushButton("选择账号")
        self.select_account_btn.setFixedHeight(30)
        self.select_account_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.select_account_btn.setStyleSheet("QPushButton:hover { color: #333; }")
        self.select_account_btn.setFixedWidth(100)
        lay.addWidget(self.select_account_btn)
        
    def setup_ui(self):
        main_widget = QWidget()
        main_hbox_layout = QHBoxLayout()
        main_widget.setLayout(main_hbox_layout)

        main_left_widget = QWidget()
        main_hbox_layout.addWidget(main_left_widget, stretch=2)

        main_right_widget = QWidget()
        main_hbox_layout.addWidget(main_right_widget, stretch=10)

        self.setup_left_area_ui(main_left_widget)
        self.setup_right_area_ui(main_right_widget)

        self.setCentralWidget(main_widget)