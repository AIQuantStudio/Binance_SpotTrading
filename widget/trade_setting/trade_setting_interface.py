from typing import Any


class TradeSettingInterface:
    def __init__(self):
        pass

    def lock_all(self):
        pass
    
    def unlock_all(self):
        pass
    
    def get_setting(self) -> Any:
        pass
    
    # @property
    # def strategy_name(self):
    #     return 