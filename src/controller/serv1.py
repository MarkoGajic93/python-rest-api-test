import random

import uvicorn
from fastapi import FastAPI

from src.models import HealthStatus

app = FastAPI()

@app.get("/healthcheck", response_model=HealthStatus)
def healthcheck():
    stats = [{"status": "healthy"}, {"status": "not healthy"}]
    return HealthStatus(**random.choice(stats))

if __name__ == "__main__":
    uvicorn.run("serv1:app", port=8000, reload=True)