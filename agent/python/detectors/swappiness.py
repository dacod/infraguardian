import subprocess

def check_swappiness():
    try:
        result = subprocess.run(["sysctl", "-n", "vm.swappiness"], capture_output=True, text=True)
        swappiness = int(result.stdout.strip())
        print(f"[Detector] Swappiness atual: {swappiness}")
        if swappiness > 10:
            return {
                "issue": "Swappiness muito alto",
                "current_value": swappiness,
                "recommended": 10,
                "fix": "fix_swap"
            }
    except Exception as e:
        print(f"[Detector] Erro: {e}")
    return None
