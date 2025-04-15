from fastapi import APIRouter
from pydantic import BaseModel
from typing import List
from datetime import datetime

router = APIRouter(prefix="/hosts", tags=["hosts"])

class HostMetrics(BaseModel):
    hostname: str
    cpu_usage: float
    ram_usage: float
    timestamp: datetime

fake_db = []

@router.post("/metrics")
def receive_metrics(metrics: HostMetrics):
    fake_db.append(metrics)
    return {"status": "ok"}

@router.get("/metrics", response_model=List[HostMetrics])
def list_metrics():
    return fake_db
