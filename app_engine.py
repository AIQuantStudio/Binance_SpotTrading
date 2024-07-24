import os
from typing import Any, Sequence, Type, Dict, List, Optional

from event import Event, EventEngine, EVENT_LOG
from service import EmailService
from service import BaseService, LogService, EmailService
from harvester.gateway import BaseGateway
from harvester.app import BaseApp
from harvester.structure import LogData, Exchange


class AppEngine:
    """"""

    def __init__(self):
        """"""
        self._event_engine = EventEngine()
        self._event_engine.start()

        self._gateways: Dict[str, BaseGateway] = {}
        self._services = {}
        self._apps: Dict[str, BaseApp]  = {}

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

    # def add_gateway(self, gateway_class: Type[BaseGateway]) -> BaseGateway:
    #     """"""
    #     gateway = gateway_class(self)
    #     self._gateways[gateway.name] = gateway
    #     return gateway

    # def add_app(self, app_class: Type[BaseApp]) -> BaseService:
    #     """"""
    #     app = app_class()
    #     self._apps[app.app_name] = app
    #     service = self.add_service(app.service_class)
    #     return service

    def get_service(self, service_name):
        """"""
        service = self._services.get(service_name, None)
        if service is None:
            print(f"找不到服务：{service_name}")
        return service

    # def get_gateway(self, gateway_name: str) -> BaseGateway:
    #     """"""
    #     gateway = self._gateways.get(gateway_name, None)
    #     if not gateway:
    #         self.write_log(f"找不到底层接口：{gateway_name}")
    #     return gateway

    # def get_all_gateways(self) -> List[BaseGateway]:
    #     """"""
    #     return list(self._gateways.values())

    # def get_all_gateway_names(self) -> List[str]:
    #     """"""
    #     return list(self._gateways.keys())

    # def get_all_apps(self) -> List[BaseApp]:
    #     """"""
    #     return list(self._apps.values())

    # def get_all_app_names(self) -> List[str]:
    #     """"""
    #     return list(self._apps.keys())

    # def get_all_exchanges(self) -> List[Exchange]:
    #     """"""
    #     return [gateway.exchange for gateway in self._gateways.values()]

    def close(self) -> None:
        """
        首先停止 event_engine, 然后依次关闭所有的 service 和 gateway
        """
        self._event_engine.stop()

        for service in self._services.values():
            service.close()

        # for gateway in self._gateways.values():
        #     gateway.close()

    # def any_gateway_connected(self) -> bool:
    #     """"""
    #     for gateway in self._gateways.values():
    #         if gateway.is_connected():
    #             return True

    #     return False

    @property
    def log_service(self):
        if self._log_service is None:
            self._log_service = self.get_service(LogService.name)

        return self._log_service

    @property
    def email_service(self):
        """"""
        if self._email_service is None:
            self._email_service = self.get_service(EmailService.name)

        return self._email_service

    # @property
    # def oms_service(self) -> OmsService:
    #     """"""
    #     if not self._oms_service:
    #         self._oms_service = self.get_service(OmsService.name)

    #     return self._oms_service

    # def write_log(self, msg: str, gateway_name: str = "") -> None:
    #     """"""
    #     self.log_service.write(msg, gateway_name)

    # def send_email(self, subject: str, content: str, receiver: str = "") -> None:
    #     """"""
    #     self.email_service.send(subject, content, receiver)
