from typing import Any, Sequence, Type, Dict

from common import singleton
from event import EventEngine
from service import BaseService, LogService, EmailService


@singleton
class AppEngineSingleton:

    def __init__(self):
        self._services : Dict[str, BaseService] = {}
        self._log_service:LogService = None
        self._email_service = None
        
    def start(self):
        self._event_engine = EventEngine()
        self._event_engine.start()

        self.add_service(LogService)
        self.add_service(EmailService)

    @property
    def event_engine(self):
        return self._event_engine

    def add_service(self, service_class):
        if issubclass(service_class, BaseService):
            service = service_class(self._event_engine)
            self._services[service.name] = service
        return service

    def get_service(self, service_name):
        service = self._services.get(service_name, None)
        if service is None:
            print(f"找不到服务：{service_name}")
        return service

    def close(self):
        self._event_engine.stop()

        for service in self._services.values():
            service.close()

    @property
    def log_service(self) -> LogService:
        if self._log_service is None:
            self._log_service = self.get_service(LogService.name)

        return self._log_service

    @property
    def email_service(self):
        if self._email_service is None:
            self._email_service = self.get_service(EmailService.name)

        return self._email_service

    def write_log(self, msg: str):
        self.log_service.write(msg)
        

AppEngine = AppEngineSingleton()