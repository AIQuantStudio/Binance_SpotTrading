from typing import Any


class TradeSettingInterface:
    def __init__(self):
        pass

    def lock_all(self):
        pass
    
    def unlock_all(self):
        pass
    
    def get_setting_data(self) -> Any:
        pass