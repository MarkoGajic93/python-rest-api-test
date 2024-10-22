import smtplib
from smtplib import SMTPException
from unittest import mock

import pytest

from src.service.notifier import EmailNotifier

@pytest.fixture
def notifier():
    return EmailNotifier()

@mock.patch("smtplib.SMTP.send_message")
def test_notify_success(mock_send_message, notifier):
    message, sent = notifier.notify(subject="Title", message_body="body", receiver="gajic.marko@yahoo.com")
    assert sent
    assert message["Subject"] == "Title"
    assert message["From"] == "gajic.marko1993@gmail.com"
    assert message["To"] == "gajic.marko@yahoo.com"
    assert message.get_content() == "body\n"

@mock.patch("smtplib.SMTP.login")
def test_notify_fail(mock_login, notifier):
    mock_login.side_effect = SMTPException
    message, sent = notifier.notify(subject="Title", message_body="body", receiver="gajic.marko@yahoo.com")
    assert not sent
    assert message["Subject"] == "Title"
    assert message["From"] == "gajic.marko1993@gmail.com"
    assert message["To"] == "gajic.marko@yahoo.com"
    assert message.get_content() == "body\n"
