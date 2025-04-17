import os
import shutil
import subprocess

def check_open_file_limits():
    try:
        with open("/proc/sys/fs/file-max") as f:
            current_limit = int(f.read().strip())
        if current_limit < 100000:
            return {
                "issue": "Limite de arquivos abertos é baixo",
                "current_value": current_limit,
                "recommended": 100000,
                "fix": "fix_file_limits"
            }
    except Exception as e:
        print(f"[Detector] Erro ao verificar file-max: {e}")
    return None

def check_disk_usage():
    try:
        total, used, free = shutil.disk_usage("/")
        percent_used = (used / total) * 100
        if percent_used > 85:
            return {
                "issue": "Uso de disco acima de 85%",
                "current_value": round(percent_used, 2),
                "recommended": "< 85%",
                "fix": "alert_disk_full"
            }
    except Exception as e:
        print(f"[Detector] Erro ao verificar uso de disco: {e}")
    return None

def check_sysctl_net_ipv4_tcp_syncookies():
    try:
        result = subprocess.run(["sysctl", "-n", "net.ipv4.tcp_syncookies"], capture_output=True, text=True)
        value = int(result.stdout.strip())
        if value == 0:
            return {
                "issue": "tcp_syncookies desativado (pode abrir brecha para SYN flood)",
                "current_value": value,
                "recommended": 1,
                "fix": "fix_syncookies"
            }
    except Exception as e:
        print(f"[Detector] Erro ao verificar tcp_syncookies: {e}")
    return None
