from threading import Thread

from trading.backtester_engine import BacktesterEngine
from structure import BacktestSettingStruct

class Backtester:
    def __init__(self):
        self._backtesting: BacktesterEngine = None
        self._thread = None
        
        self.backtest_setting_data: BacktestSettingStruct = None
    
    def init(self, data):
        self._backtesting = BacktesterEngine(data)
        
        
    def start(self):
        if self._thread is None:
            # self._write_log("已有任务在运行中，请等待完成")
            return False

        self._thread = Thread(target=self._run)
        self._thread.start()

    def run(self):
        self._backtesting.clear_data()
        self._backtesting.load_history_data()

        try:
            self._backtesting.run_backtesting()
        except Exception:
            # self._write_log(f"策略回测失败，触发异常：\n{traceback.format_exc()}")
            self._thread = None
            return

        self.result_df = self._backtesting.calculate_result()
        self.result_statistics = self._backtesting.calculate_statistics(output=False)

        self._thread = None

        if self._signal_backtesting_finished:
            self._signal_backtesting_finished.emit()
            
    def resume(self):
        pass

    def stop(self):
        pass
    
    def close(self):
        pass