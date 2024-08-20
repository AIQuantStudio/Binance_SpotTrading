import smtplib
from functools import partial
from queue import Empty
from email.message import EmailMessage
from PyQt6 import QtCore

from config import Config
from event import EventEngine

from service.base_service import BaseService


class EmailService(BaseService):

    name = "email"
    
    def __init__(self, event_engine: EventEngine):
        super().__init__()
        
        self.event_engine = event_engine
    

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
