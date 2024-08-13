from typing import Any

EVENT_UNSUBSCRIBE = "eUnsubscribe."
EVENT_TICK = "eTick."
EVENT_TRADE = "eTrade."
EVENT_ORDER = "eOrder."
EVENT_POSITION = "ePosition."
EVENT_ACCOUNT = "eAccount."
EVENT_CONTRACT = "eContract."
EVENT_LOG = "eLog"
EVENT_TIMER = "eTimer"

EVENT_MARKETMANAGER_UPDATE = "eMarketManagerUpdate"
EVENT_MARKETMANAGER_EXCEPTION = "eMarketManagerException"

EVENT_TRADER_STRATEGY = "evtTraderStrategy"
EVENT_TRADER_STOPORDER = "evtTraderStopOrder"



EVENT_ASSET_BALANCE = "eAssetBalance"
EVENT_PREDICT = "ePredict"


EVENT_TIMER = "eTimer"
EVENT_ASYNC = "eAsync"

class Event:

    def __init__(self, type, data = None):
        self.type = type
        self.data = data

