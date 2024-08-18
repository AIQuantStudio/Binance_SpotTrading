import threading


class TradingDaemon:
    
    def __init__(self, model_id):
        super().__init__()
        
        self.model_id = model_id
        self.thread_alive = False
        self.thread = threading.Thread(target=self.run, daemon=True)
        

    def run(self):
        while self.thread_alive:
            last_close_price = 1
            predict_price = 2
            
        
    def start(self):
        self.thread_alive = True
        self.thread.start()
        
    def stop(self):
        self.thread_alive = False
        self.thread.join()
