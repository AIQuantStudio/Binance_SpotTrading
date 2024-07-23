from PyQt6.QtCore import QThread, QObject, pyqtSlot, pyqtSignal


 
class WorkerSignals(QObject):
    finished = pyqtSignal()
    result = pyqtSignal(object)
 
class Worker(QObject):
    def __init__(self, fn):
        super().__init__()
        self.fn = fn
    @pyqtSlot()
    def run(self):
        self.fn()  # Your asynchronous function here
        self.finished.emit()
 
class AsyncMarket(QThread):
    def __init__(self, result_signal, fn, *args, **kwargs):
        super(QThread, self).__init__()
        self.fn = fn
        self.args = args
        self.kwargs = kwargs
        self.signals = WorkerSignals()
        self.worker = Worker(self.fn)
        self.worker.moveToThread(self)
        self.signals.finished.connect(self.quit)
        self.signals.result.connect(self.handle_result)
        self.started.connect(self.worker.run)
 
    def handle_result(self, result):
        print(f"Result: {result}")
 
    def run(self):
        self.exec_()
        
        
        
class MarketWorker(QThread):

    def __init__(self):
        super(MarketWorker, self).__init__()

        self.working = False


    def start(self, unames, respTimeout, token):
        self.usernames = unames
        self.token = token
        self.respTimeout = (int(respTimeout) / 1000.0)
        super().start()

    def stop(self):
        self.working = False

    def run(self):
        global CounterGC
        try:
            self.working = True
            while(self.working):
                Mtx.lock()
                CounterGC = CounterGC + 1
                if CounterGC > GC_MAX_COUNT:
                    self.gcCacheRecords()
                    CounterGC = 0
                Mtx.unlock()

                self.requestRecords()
                time.sleep(0.2)
        except Exception as e:
            self.webEngine.printLog(f'管理平台[{self.id}]异常:{e}')
            print(f'MakeTask {e}')