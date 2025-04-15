import psutil
import requests
import socket
from datetime import datetime

API_URL = "http://localhost:8000/hosts/metrics"

def collect_metrics():
    hostname = socket.gethostname()
    cpu = psutil.cpu_percent(interval=1)
    ram = psutil.virtual_memory().percent
    timestamp = datetime.utcnow().isoformat()

    payload = {
        "hostname": hostname,
        "cpu_usage": cpu,
        "ram_usage": ram,
        "timestamp": timestamp
    }

    response = requests.post(API_URL, json=payload)
    print(f"[{timestamp}] Enviado: CPU {cpu}%, RAM {ram}% – Status: {response.status_code}")

if __name__ == "__main__":
    collect_metrics()
