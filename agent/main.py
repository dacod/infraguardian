import psutil
import requests
import socket
from datetime import datetime
from detectors import swappiness, sys_health

API_URL = "http://localhost:8000/hosts/metrics"

def run_all_detectors():
    detectors = [
        # swappiness.check_swappiness,
        sys_health.check_open_file_limits,
        sys_health.check_disk_usage,
        sys_health.check_sysctl_net_ipv4_tcp_syncookies
    ]
    for detector in detectors:
        issue = detector()
        if issue:
            fix_payload = {
                "hostname": socket.gethostname(),
                "timestamp": datetime.now().isoformat(),
                "issue": issue["issue"],
                "current_value": issue["current_value"],
                "recommended": issue["recommended"],
                "fix": issue["fix"]
            }
            requests.post("http://localhost:8000/hosts/fix", json=fix_payload)



def collect_metrics():
    hostname = socket.gethostname()
    cpu = psutil.cpu_percent(interval=1)
    ram = psutil.virtual_memory().percent
    timestamp = datetime.now().isoformat()

    payload = {
        "hostname": hostname,
        "cpu_usage": cpu,
        "ram_usage": ram,
        "timestamp": timestamp
    }

    requests.post(API_URL, json=payload)

    # Verifica problemas
    issue = swappiness.check_swappiness()
    if issue:
        fix_payload = {
            "hostname": hostname,
            "timestamp": timestamp,
            "issue": issue["issue"],
            "current_value": issue["current_value"],
            "recommended": issue["recommended"],
            "fix": issue["fix"]
        }
        requests.post("http://localhost:8000/hosts/fix", json=fix_payload)
        run_all_detectors()


if __name__ == "__main__":
    collect_metrics()

