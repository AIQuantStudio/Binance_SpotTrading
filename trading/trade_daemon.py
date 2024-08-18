from PyQt6.QtCore import *


class TradeDaemon(QThread):
    
    def __init__(self, model_id):
        super().__init__()
        
        self.model_id = model_id

    def run(self):
        while True:
            pass
        
    def start(self):
        super().start()
