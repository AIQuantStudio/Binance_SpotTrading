import traceback
from collections import defaultdict
from queue import Empty, Queue
from threading import Thread
from time import sleep

from event.event import Event, EVENT_TIMER


class EventEngine:

    def __init__(self):
        self.active = False
        self.event_queue = Queue()
        
        self.event_thread = Thread(target=self.event_loop)
        self.event_timer = Thread(target=self.timer_loop)
        
        self.event_handler_map = defaultdict(list)
        self.general_handler_list = []

    def event_loop(self):
        while self.active:
            try:
                event = self.event_queue.get(block=True, timeout=1)
                
                # 事件机制优化处理，处理已断的信号事件，并清除
                if event.type in self.event_handler_map:
                    for handler in self.event_handler_map[event.type]:
                        try:
                            handler(event)
                        except:
                            if (handler is None) or (not callable(handler)):
                                self.event_handler_map[event.type].remove(handler)
                            else:
                                print(f"事件响应失败[{event.type}] \n {traceback.format_exc()}")
                                
                if self.general_handler_list:
                    for handler in self.general_handler_list:
                        try:
                            handler(event)
                        except:
                            if (handler is None) or (not callable(handler)):
                                self.general_handler_list.remove(handler)
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

    def register(self, type, handler):
        if not callable(handler):
            return
        
        handler_list = self.event_handler_map[type]
        if handler not in handler_list:
            handler_list.append(handler)

    def unregister(self, type, handler):
        handler_list = self.event_handler_map[type]
        if handler in handler_list:
            handler_list.remove(handler)

        if not handler_list:
            self.event_handler_map.pop(type)

    def register_general(self, handler):
        if not callable(handler):
            return
        
        if handler not in self.general_handler_list:
            self.general_handler_list.append(handler)

    def unregister_general(self, handler):
        if handler in self.general_handler_list:
            self.general_handler_list.remove(handler)
