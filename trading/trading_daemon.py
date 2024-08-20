from threading import Thread

from trading.backtester_engine import BacktesterEngine
from event import EVENT_MAKE_ORDER, EVENT_DEAL_ORDER
from structure import TradeSettingMode
from app_engine import AppEngine


class TradingDaemon:
    
    def __init__(self, model_id,  setting_mode, setting_data):
        super().__init__()
        
        self.model_id = model_id
        self.setting_mode = setting_mode
        self.setting_data = setting_data
        
        self.backtesting = None
        self.thread = None

        # self.thread = threading.Thread(target=self.run, daemon=True)
        
    def start(self):  
        if self.setting_mode == TradeSettingMode.NORMAL:
            pass
        elif self.setting_mode == TradeSettingMode.TEST:
            self.backtesting = BacktesterEngine(self.model_id, self.setting_data)
            # self.backtester.start()
            
            if self.thread is not None:
                # self._write_log("已有任务在运行中，请等待完成")
                return False

            self.thread = Thread(target=self.run, daemon=True)
            self.thread.start()
            
    def run(self):
        self.backtesting.clear_data()
        self.backtesting.load_history_data()

        try:
            self.backtesting.run_backtesting()
        except Exception:
            # self._write_log(f"策略回测失败，触发异常：\n{traceback.format_exc()}")
            self.thread = None
            return

        self.result_df = self._backtesting.calculate_result()
        self.result_statistics = self._backtesting.calculate_statistics(output=False)

        self.thread = None

        if self._signal_backtesting_finished:
            self._signal_backtesting_finished.emit()
            
    
    def stop(self):
        # AppEngine.event_engine.unregister(self.process_make_order)
        # AppEngine.event_engine.unregister(self.process_deal_order)
        self.thread_alive = False
        # self.thread.join()

    def resume(self):
        pass

    def close(self):
        pass

    def process_make_order(self):
        pass
    
    def process_deal_order(self):
        pass