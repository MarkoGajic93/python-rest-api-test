import smtplib
from abc import ABC, abstractmethod
from configparser import ConfigParser
from email.message import EmailMessage

from typing_extensions import override


class Notifier(ABC):
    @abstractmethod
    def notify(self, subject: str, message_body: str, receiver: str):
        ...

class EmailNotifier(Notifier):
    def __init__(self):
        config = ConfigParser()
        config.read("C:/Users/mgajic/PycharmProjects/apiProject_v2/src/config/config.ini")
        self._gmail_username = config["email"]["gmail_username"]
        self._gmail_app_password = config["email"]["gmail_app_password"]

    @override
    def notify(self, subject: str, message_body: str, receiver: str) -> tuple[EmailMessage, bool]:
        msg = self._create_email_message(subject=subject, message_body=message_body, to_email=receiver)
        sent = self._send_email(msg)
        return msg, sent

    def _create_email_message(self, subject: str, message_body: str, to_email: str) -> EmailMessage:
        message = EmailMessage()
        message["From"] = self._gmail_username
        message["Subject"] = subject
        message.set_content(message_body)
        message["To"] = to_email
        return message

    def _send_email(self, message: EmailMessage) -> bool:
        try:
            with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
                smtp.login(user=self._gmail_username, password=self._gmail_app_password)
                smtp.send_message(message)
                print("Email sent successfully.")
                return True
        except Exception as e:
            print(f"Error sending email {e}")
            return False
