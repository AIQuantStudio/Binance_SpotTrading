import logging
from pathlib import Path
from datetime import datetime

from config import Config
from structure import LogStruct
from event import EventEngine, Event, EVENT_LOG

from service.base_service import BaseService


class LogService(BaseService):

    def __init__(self, event_engine: EventEngine):
        super().__init__("log")

        self.event_engine = event_engine

        if not Config.get("log.active"):
            return

        self.logger = logging.getLogger("Logger")
        self.level = Config.get("log.level")
        self.formatter = logging.Formatter(Config.get("log.formatter"))
        self.logger.setLevel(self.level)

        self.add_null_handler()

        if Config.get("log.console"):
            self.add_console_handler()

        if Config.get("log.file"):
            self.add_file_handler()

        self.event_engine.register(EVENT_LOG, self.process_log_event)

    def add_null_handler(self):
        null_handler = logging.NullHandler()
        self.logger.addHandler(null_handler)

    def add_console_handler(self):
        console_handler = logging.StreamHandler()
        console_handler.setLevel(self.level)
        console_handler.setFormatter(self.formatter)
        self.logger.addHandler(console_handler)

    def add_file_handler(self):
        filename = f"log_{datetime.now().strftime('%Y%m%d')}.log"
        log_path = Path(".").joinpath("log")
        if not log_path.exists():
            log_path.mkdir()

        file_path = log_path.joinpath(filename)

        file_handler = logging.FileHandler(file_path, mode="a", encoding="utf8")
        file_handler.setLevel(self.level)
        file_handler.setFormatter(self.formatter)
        self.logger.addHandler(file_handler)

    def process_log_event(self, event: Event):
        log: LogStruct = event.data
        self.logger.log(log.level, log.msg)

    def write(self, msg: str):
        event = Event(EVENT_LOG, LogStruct(msg=msg))
        self.event_engine.put(event)

    def close(self):
        self.event_engine.unregister(EVENT_LOG, self.process_log_event)
        super().close()
