import logging
from pathlib import Path
from datetime import datetime

from config import Config_Data
from event import EVENT_LOG
# from harvester.setting import Setting
# from harvester.structure import LogData

from service.base_service import BaseService


class LogService(BaseService):

    def __init__(self, app_engine):
        super().__init__("log")

        self.app_engine = app_engine

        if not Config_Data["log.active"]:
            return

        self.logger = logging.getLogger("Logger")
        self.level = Config_Data["log.level"]
        self.formatter = logging.Formatter(Config_Data["log.formatter"])
        self.logger.setLevel(self.level)

        self.add_null_handler()

        if Config_Data["log.console"]:
            self.add_console_handler()

        if Config_Data["log.file"]:
            self.add_file_handler()

        # self._register_event()
        self.app_engine.event_engine.register(EVENT_LOG, self.process_log_event)

    def add_null_handler(self):
        null_handler = logging.NullHandler()
        self.logger.addHandler(null_handler)

    def add_console_handler(self):
        console_handler = logging.StreamHandler()
        console_handler.setLevel(self.level)
        console_handler.setFormatter(self.formatter)
        self.logger.addHandler(console_handler)

    def add_file_handler(self) -> None:
        filename = f"log_{datetime.now().strftime('%Y%m%d')}.log"
        log_path = Path(".").joinpath("log")
        if not log_path.exists():
            log_path.mkdir()

        file_path = log_path.joinpath(filename)

        file_handler = logging.FileHandler(file_path, mode="a", encoding="utf8")
        file_handler.setLevel(self.level)
        file_handler.setFormatter(self.formatter)
        self.logger.addHandler(file_handler)

    # def _register_event(self) -> None:
    #     self._event_engine.register(EVENT_LOG, self._process_log_event)

    def process_log_event(self, event):
        log = event.data
        self.logger.log(log.level, log.msg)

    # def write(self, msg: str, gateway_name: str = "") -> None:
    #     event = Event(EVENT_LOG, LogData(msg=msg, gateway_name=gateway_name))
    #     self._event_engine.put(event)

    def close(self):
        super().close()