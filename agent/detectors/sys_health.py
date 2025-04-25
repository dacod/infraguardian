import os
import shutil
import subprocess

def check_open_file_limits():
    try:
        with open("/proc/sys/fs/file-max") as f:
            current_limit = int(f.read().strip())
        print(f"[Detector] Limite de arquivos abertos: {current_limit}")
        if current_limit < 100000:
            print(f"**______ [Alerta] ALERTA LIMITE DE ARQUIVOS: {current_limit}")
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
        print(f"[Detector] Uso de disco: {percent_used:.2f}%")
        if percent_used > 85:
            print(f"**______ [Alerta] ALERTA DE DISCO: {percent_used}")
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
        print(f"[Detector] tcp_syncookies: {value}")
        if value == 0:
            print(f"**______ [Alerta] tcp_syncookies WARN")
            return {
                "issue": "tcp_syncookies desativado (pode abrir brecha para SYN flood)",
                "current_value": value,
                "recommended": 1,
                "fix": "fix_syncookies"
            }
    except Exception as e:
        print(f"[Detector] Erro ao verificar tcp_syncookies: {e}")
    return None
