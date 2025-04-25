from fastapi import APIRouter
from pydantic import BaseModel
from typing import List, Union
from datetime import datetime
import subprocess


router = APIRouter(prefix="/hosts", tags=["hosts"])

class HostMetrics(BaseModel):
    hostname: str
    cpu_usage: float
    ram_usage: float
    timestamp: datetime
    swappiness: int | None = None
    sys_health: dict | None = None


class FixRequest(BaseModel):
    hostname: str
    timestamp: str
    issue: str
    current_value: Union[str, int, float]
    recommended: Union[str, int, float]
    fix: str


fix_map = {
    "fix_swap": "fix_swap.yml",
    "fix_file_limits": "fix_file_limits.yml",
    "fix_syncookies": "fix_syncookies.yml",
    "alert_disk_full": "alert_disk_full.yml"
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
    # print(f"[DEBUG] DATA: {data}")
    if playbook:
        print("[DEBUG] ===> RODANDO PLAYBOOK:", playbook)
        try:
            print(f"[API] Correção aplicada: {data.issue}")
            print(f"[API] Saída do playbook: {result.stdout}")
            result = subprocess.run([
                "ansible-playbook", f"ansible/playbooks/{playbook}", "-i", "ansible/inventory/hosts.ini",
            ], capture_output=True, text=True)
            return {"status": "fix applied", "output": result.stdout}
        except Exception as e:
            return {"status": "error", "message": str(e)}
    elif data.fix == "alert_disk_full":
        print(f"[ALERTA] Uso de disco alto detectado no host {data.hostname}")
        return {"status": "alert only"}
    else:
        return {"status": "unknown fix"}