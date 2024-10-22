import asyncio
from datetime import datetime

from src.http_client import HttpClient
from src.service.notifier import Notifier


class HealthStatusMonitor:
    def __init__(self, http_client: HttpClient, notifier: Notifier):
        self.http_client = http_client
        self.data = []
        self.notifier = notifier

    def get_health_history(self):
        return self.data

    async def ping_healthcheck(self):
        while True:
            status_code, response = self.http_client.get("/healthcheck")
            if response["status"] == "not healthy":
                self.notifier.notify(subject="Health status warning",
                                     message_body=f"Health monitor detected status: {response["status"]}\n"
                                                  f"for URL: {self.http_client.base_url}\n"
                                                  f"at {datetime.now()}",
                                     receiver="gajic.marko@yahoo.com")
            self.data.append({"timestamp": datetime.now(), "status": response["status"]})
            await asyncio.sleep(10)