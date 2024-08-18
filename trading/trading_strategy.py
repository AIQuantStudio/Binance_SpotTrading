from structure import TradingDecision


class TradingStrategy:
    
    def __init__(self, mode):
        self.mode = mode
        
    def set_last_price(self, last_price):
        self.last_price = last_price
        
    def set_predict_price(self, predict_price):
        self.predict_price = predict_price
        
    def decide(self):
        decision = TradingDecision.EMPTY
        if self.predict_price > self.last_price:
            decision = TradingDecision.BUY
        elif self.predict_price < self.last_price:
            decision = TradingDecision.SELL
        
    
        
        
    
        
        