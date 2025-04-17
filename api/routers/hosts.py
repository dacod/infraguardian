from fastapi import APIRouter
from pydantic import BaseModel
from typing import List
from datetime import datetime
import subprocess


router = APIRouter(prefix="/hosts", tags=["hosts"])

class HostMetrics(BaseModel):
    hostname: str
    cpu_usage: float
    ram_usage: float
    timestamp: datetime
    swappiness: int | None = None


class FixRequest(BaseModel):
    hostname: str
    timestamp: datetime
    issue: str
    current_value: int
    recommended: int
    fix: str



fake_db = []

@router.post("/metrics")
def receive_metrics(metrics: HostMetrics):
    fake_db.append(metrics)
    return {"status": "ok"}

@router.get("/metrics", response_model=List[HostMetrics])
def list_metrics():
    return fake_db

@router.post("/fix")
def apply_fix(data: FixRequest):
    if data.fix == "fix_swap":
        try:
            result = subprocess.run([
                "ansible-playbook", "ansible/playbooks/fix_swap.yml", "-i", "localhost,"
            ], capture_output=True, text=True)
            print(f"[API] Correção aplicada: {data.issue}")
            return {"status": "fix applied", "output": result.stdout}
        except Exception as e:
            return {"status": "error", "message": str(e)}
    return {"status": "unknown fix"}