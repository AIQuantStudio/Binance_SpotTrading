from event import EventEngine
from service import BaseService, LogService, EmailService


class AppEngine:

    def __init__(self):
        self._event_engine = EventEngine()
        self._event_engine.start()

        self._services = {}
        self._log_servic = None
        self._email_service = None

        self.add_service(LogService)
        self.add_service(EmailService)

    @property
    def event_engine(self):
        return self._event_engine

    def add_service(self, service_class):
        if issubclass(service_class, BaseService):
            service = service_class(self)
            self._services[service.name] = service
        return service

    def get_service(self, service_name):
        service = self._services.get(service_name, None)
        if service is None:
            print(f"找不到服务：{service_name}")
        return service

    def close(self):
        """ 首先停止 event_engine, 然后依次关闭所有的 service """
        self._event_engine.stop()

        for service in self._services.values():
            service.close()

    @property
    def log_service(self):
        if self._log_service is None:
            self._log_service = self.get_service(LogService.name)

        return self._log_service

    @property
    def email_service(self):
        if self._email_service is None:
            self._email_service = self.get_service(EmailService.name)

        return self._email_service
