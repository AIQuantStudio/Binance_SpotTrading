import traceback
from collections import defaultdict
from queue import Empty, Queue
from threading import Thread
from time import sleep
from typing import Any, Callable, List

from event.event import Event, EVENT_TIMER


HandlerType = Callable[[Event], None]


class EventEngine:

    def __init__(self):
        """"""
        self.active = False
        
        
        self.event_queue = Queue()
        
        self.event_thread = Thread(target=self.event_loop)
        self.event_timer = Thread(target=self.timer_loop)
        self._handlers: defaultdict = defaultdict(list)
        self._general_handlers = []

    def event_loop(self):
        """"""
        while self.active:
            try:
                event = self.event_queue.get(block=True, timeout=1)
                
                # 事件机制优化处理，处理已断的信号事件，并清除
                if event.type in self._handlers:
                    for handler in self._handlers[event.type]:
                        try:
                            handler(event)
                        except:
                            if (None is handler) or not callable(handler):
                                self._handlers[event.type].remove(handler)
                            else:
                                print(f"事件响应失败[{event.type}] \n {traceback.format_exc()}")
                                
                if self._general_handlers:
                    for handler in self._general_handlers:
                        try:
                            handler(event)
                        except:
                            if (None is handler) or not callable(handler):
                                self._general_handlers.remove(handler)
                            else:
                                print(f"通用事件响应失败[{event.type}] \n {traceback.format_exc()}")
            except Empty:
                pass

    def timer_loop(self):
        """ 计时器事件(EVENT_TIMER) """
        sleep_interval = 1
        while self.active:
            sleep(sleep_interval)
            event = Event(EVENT_TIMER)
            self.put(event)

    def start(self):
        self.active = True
        self.event_thread.start()
        self.event_timer.start()

    def stop(self):
        self.active = False
        self.event_timer.join()
        self.event_thread.join()

    def put(self, event: Event):
        self.event_queue.put(event)

    def register(self, type, handler: HandlerType):
        """
        为特定事件类型注册新的处理程序函数，对于同一个事件类型的函数只能注册一次
        """
        handler_list = self._handlers[type]
        if handler not in handler_list:
            handler_list.append(handler)

    def unregister(self, type, handler: HandlerType):
        """
        从事件引擎注销处理程序函数
        """
        handler_list = self._handlers[type]

        if handler in handler_list:
            handler_list.remove(handler)

        if not handler_list:
            self._handlers.pop(type)

    def register_general(self, handler: HandlerType):
        """
        注册一般处理程序函数，对于每个一般处理函数只能注册一次
        """
        if handler not in self._general_handlers:
            self._general_handlers.append(handler)

    def unregister_general(self, handler: HandlerType):
        """
        从事件引擎注销一般处理程序函数
        """
        if handler in self._general_handlers:
            self._general_handlers.remove(handler)
