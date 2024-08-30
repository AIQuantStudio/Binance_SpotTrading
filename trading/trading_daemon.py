from threading import Thread

from trading.backtester import Backtester
from event import EVENT_MAKE_ORDER, EVENT_DEAL_ORDER
from structure import TradeMode
from main_engine import MainEngine


class TradingDaemon:
    
    def __init__(self, model_id,  trade_mode, strategy, setting_data):
        super().__init__()
        
        self.model_id = model_id
        self.strategy = strategy
        self.trade_mode = trade_mode
        self.setting_data = setting_data
        
        self.backtester = None
        self.thread = None

        # self.thread = threading.Thread(target=self.run, daemon=True)
        
    def start(self):  
        if self.trade_mode == TradeMode.TRADER:
            pass
        elif self.trade_mode == TradeMode.BACKTESTER:
            self.backtester = Backtester(self.model_id, self.strategy, self.setting_data)
            
            if self.thread is not None:
                # self._write_log("已有任务在运行中，请等待完成")
                return False

            self.thread = Thread(target=self.run_backtester, daemon=True)
            self.thread.start()
            
    def run_backtester(self):
        self.backtester.clear_data()
        self.backtester.load_history_data()

        self.backtester.run_strategy()
        # try:
        #     self.backtester.run_strategy()
        # except Exception:
        #     # self._write_log(f"策略回测失败，触发异常：\n{traceback.format_exc()}")
        #     self.thread = None
        #     return

        # self.backtester.calculate_statistics()
        
        # self.result_df = self._backtesting.calculate_result()
        # self.result_statistics = self._backtesting.calculate_statistics(output=False)

        
        self.thread = None

        # if self._signal_backtesting_finished:
        #     self._signal_backtesting_finished.emit()
            
    
    def stop(self):
        pass
        # MainEngine.event_engine.unregister(self.process_make_order)
        # MainEngine.event_engine.unregister(self.process_deal_order)
        # self.thread_alive = False
        # self.thread.join()

    def resume(self):
        pass

    def close(self):
        pass

    def process_make_order(self):
        pass
    
    def process_deal_order(self):
        pass
    
    @property
    def is_running(self):
        return self.thread is not None and self.thread.is_alive()
            