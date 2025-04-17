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

fix_map = {
    "fix_swap": "fix_swap.yml",
    "fix_file_limits": "fix_file_limits.yml",
    "fix_syncookies": "fix_syncookies.yml"
}

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
    playbook = fix_map.get(data.fix)
    if playbook:
        try:
            result = subprocess.run([
                "ansible-playbook", f"ansible/playbooks/{playbook}", "-i", "localhost,"
            ], capture_output=True, text=True)
            print(f"[API] Correção aplicada: {data.issue}")
            return {"status": "fix applied", "output": result.stdout}
        except Exception as e:
            return {"status": "error", "message": str(e)}
    elif data.fix == "alert_disk_full":
        print(f"[ALERTA] Uso de disco alto detectado no host {data.hostname}")
        return {"status": "alert only"}
    return {"status": "unknown fix"}