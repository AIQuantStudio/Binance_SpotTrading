import threading

from trading.backtester import Backtester 
from event import EVENT_MAKE_ORDER, EVENT_DEAL_ORDER
from structure import TradeSettingMode

class TradingDaemon:
    
    def __init__(self, app_engine, model_id, setting_mode, setting_data):
        super().__init__()
        self.app_engine = app_engine
        self.model_id = model_id
        self.setting_mode = setting_mode
        self.setting_data = setting_data
        self.thread_alive = False
        self.thread = threading.Thread(target=self.run, daemon=True)
        
    def run(self):
        while self.thread_alive:
            last_close_price = 1
            predict_price = 2
            
    def start(self):
        if self.setting_mode == TradeSettingMode.NORMAL:
            pass
        elif self.setting_mode == TradeSettingMode.TEST:
            self.backtester = Backtester()
            self.backtester.start()

        self.thread_alive = True
        self.thread.start()
        
    def stop(self):
        self.app_engine.event_engine.unregister(self.process_make_order)
        self.app_engine.event_engine.unregister(self.process_deal_order)
        self.thread_alive = False
        self.thread.join()

    def process_make_order(self):
        pass
    
    def process_deal_order(self):
        pass