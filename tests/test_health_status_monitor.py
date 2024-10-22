import asyncio
import random
from unittest import mock

import pytest

from src.http_client import HttpClient
from src.service.health_monitor import HealthStatusMonitor
from src.service.notifier import EmailNotifier

@pytest.mark.asyncio
@mock.patch("src.service.notifier.EmailNotifier.notify")
@mock.patch("src.http_client.HttpClient.get")
async def test_ping_healthcheck(mock_get, mock_notify):
    mock_get.return_value = (200, random.choice([{"status": "healthy"}, {"status": "not healthy"}]))
    monitor = HealthStatusMonitor(HttpClient("some_url"), EmailNotifier())
    with pytest.raises(asyncio.TimeoutError):
        await asyncio.wait_for(monitor.ping_healthcheck(), timeout=21)

    assert len(monitor.get_health_history()) == 3