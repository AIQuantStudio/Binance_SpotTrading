import smtplib
from threading import Thread
from queue import Empty, Queue
from email.message import EmailMessage

from harvester.setting import Setting

from config import Config_Data

from service.base_service import BaseService


class EmailService(BaseService):
    """"""

    name = "email"

    def __init__(self, main_engine):
        """"""
        super().__init__()

        self.thread: Thread = Thread(target=self._run)
        self.queue: Queue = Queue()
        self.active: bool = False

    def _run(self) -> None:
        """"""
        while self.active:
            try:
                msg = self.queue.get(block=True, timeout=1)

                with smtplib.SMTP_SSL(Config_Data.get_global_setting("email.server"), Setting.get_global_setting("email.port")) as smtp:
                    smtp.login(Setting.get_global_setting("email.username"), Setting.get_global_setting("email.password"))
                    smtp.send_message(msg)
            except Empty:
                pass

    def _start(self) -> None:
        """"""
        self.active = True
        self.thread.start()

    def close(self) -> None:
        """ 重写 BaseService::close """
        if not self.active:
            return

        self.active = False
        self.thread.join()

    def send(self, subject: str, content: str, receiver: str = "") -> None:
        """"""
        if not self.active:
            self._start()

        if not receiver:
            receiver = Setting.get_global_setting("email.receiver")

        msg = EmailMessage()
        msg["From"] = Setting.get_global_setting("email.sender")
        msg["To"] = receiver
        msg["Subject"] = subject
        msg.set_content(content)

        self.queue.put(msg)
