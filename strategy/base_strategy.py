from abc import ABC, abstractmethod
from copy import copy
from typing import Any, Callable



from main_engine import MainEngine
from event import Event, EVENT_LOG
from structure import LogStruct, BarStruct, Interval


class BaseStrategy(ABC): 

    def __init__(self, app_id):
        self.app_id = app_id
    
    @abstractmethod
    def on_init(self):
        pass
    
    @abstractmethod
    def preload(self):
        pass
    
    @abstractmethod
    def on_start(self):
        pass

    @abstractmethod
    def on_stop(self):
        pass

    @abstractmethod
    def on_bar(self, bar: BarStruct):
        pass

    def write_log(self, msg):
        MainEngine.write_log(msg)
        MainEngine.event_engine.put(event=Event(EVENT_LOG, LogStruct(msg=msg)), suffix=self.app_id)