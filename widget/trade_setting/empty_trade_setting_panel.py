from PyQt6.QtCore import *
from PyQt6.QtWidgets import *
from PyQt6.QtGui import *

from widget.trade_setting.trade_setting_interface import TradeSettingInterface



class EmptyTradeSettingPanel(QFrame, TradeSettingInterface):

    def __init__(self, parent_widget, top_dock):
        QFrame.__init__(self, parent_widget)
        
        self.top_dock = top_dock

        self.setLineWidth(2)
        self.setMidLineWidth(2)
        self.setFrameStyle(QFrame.Shape.Panel | QFrame.Shadow.Sunken)

    def lock_all(self):
        pass
    

    def unlock_all(self):
        pass

    def get_setting_data(self):
        pass