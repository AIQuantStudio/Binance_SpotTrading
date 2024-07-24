import logging
from datetime import datetime

import harvester
from harvester.event import Event, EVENT_LOG
from harvester.setting import Setting
from harvester.structure import LogData

from .base import BaseService


class LogService(BaseService):
    """"""

    name = "log"

    def __init__(self, app_engine):
        """"""
        super().__init__()

        self._event_engine = app_engine.event_engine

        if not Setting.get_global_setting("log.active"):
            return

        self.level: int = Setting.get_global_setting("log.level")

        self.logger: logging.Logger = logging.getLogger("Harvester")
        self.logger.setLevel(self.level)

        self.formatter = logging.Formatter(Setting.get_global_setting("log.formatter"))

        self._add_null_handler()

        if Setting.get_global_setting("log.console"):
            self._add_console_handler()

        if Setting.get_global_setting("log.file"):
            self._add_file_handler()

        self._register_event()

    def _add_null_handler(self) -> None:
        """"""
        null_handler = logging.NullHandler()
        self.logger.addHandler(null_handler)

    def _add_console_handler(self) -> None:
        """"""
        console_handler = logging.StreamHandler()
        console_handler.setLevel(self.level)
        console_handler.setFormatter(self.formatter)
        self.logger.addHandler(console_handler)

    def _add_file_handler(self) -> None:
        """"""
        filename = f"log_{datetime.now().strftime('%Y%m%d')}.log"
        log_path = harvester.ROOT_DIR.joinpath("log")
        if not log_path.exists():
            log_path.mkdir()

        file_path = log_path.joinpath(filename)

        file_handler = logging.FileHandler(file_path, mode="a", encoding="utf8")
        file_handler.setLevel(self.level)
        file_handler.setFormatter(self.formatter)
        self.logger.addHandler(file_handler)

    def _register_event(self) -> None:
        """"""
        self._event_engine.register(EVENT_LOG, self._process_log_event)

    def _process_log_event(self, event: Event) -> None:
        """"""
        log = event.data
        self.logger.log(log.level, log.msg)

    def write(self, msg: str, gateway_name: str = "") -> None:
        """"""
        event = Event(EVENT_LOG, LogData(msg=msg, gateway_name=gateway_name))
        self._event_engine.put(event)
