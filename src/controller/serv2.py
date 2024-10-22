import asyncio
from contextlib import asynccontextmanager
from datetime import datetime

import uvicorn
from fastapi import FastAPI

from src.http_client import HttpClient
from src.service.health_monitor import HealthStatusMonitor
from src.service.notifier import EmailNotifier


@asynccontextmanager
async def lifespan(app: FastAPI):
    asyncio.create_task(monitor.ping_healthcheck())
    print(f"Health monitoring started in background at: {datetime.now()}")
    yield

app = FastAPI(lifespan=lifespan)

client = HttpClient(base_url="http://127.0.0.1:8000")
notifier = EmailNotifier()
monitor = HealthStatusMonitor(http_client=client, notifier=notifier)

@app.get("/healthcheck-history")
def get_healthcheck_history():
    return monitor.get_health_history()


if __name__ == "__main__":
    uvicorn.run("serv2:app", port=8080, reload=True)