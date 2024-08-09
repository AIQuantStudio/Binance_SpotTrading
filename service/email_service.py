import smtplib
from threading import Thread
from functools import partial
from queue import Empty, Queue
from email.message import EmailMessage
from PyQt6 import QtCore

# from harvester.setting import Setting
from config import Config

from service.base_service import BaseService


class EmailService(BaseService):

    def __init__(self, app_engine):
        super().__init__("email")
    

    def send(self, subject, content, receiver = ""):
        if not receiver:
            receiver = Config.get("email.receiver")

        msg = EmailMessage()
        msg["From"] = Config.get("email.sender")
        msg["To"] = receiver
        msg["Subject"] = subject
        msg.set_content(content)

        QtCore.QTimer(self).singleShot(0, partial(self.do_send_email, msg))
        
    def do_send_email(self, msg):
        try:
            with smtplib.SMTP_SSL(Config.get("email.server"),  Config.get("email.port")) as smtp:
                smtp.login(Config.get("email.username"), Config.get("email.password"))
                smtp.send_message(msg)
        except Empty:
            pass
    
    def close(self):        
        super().close()
