import time
import re
import platform
import subprocess
import requests

PAINEL_URL = "https://painel-api-k2v2.onrender.com/command"
SLEEP_INTERVAL = 5  # segundos

def get_mac():
    try:
        if platform.system() == "Windows":
            output = subprocess.check_output("getmac", encoding="cp1252", errors="ignore")
            macs = re.findall(r"([0-9A-Fa-f]{2}[-:]){5}[0-9A-Fa-f]{2}", output)
            return macs[0].replace("-", ":").lower() if macs else None
        else:
            output = subprocess.check_output("ifconfig", encoding="utf-8", errors="ignore")
            macs = re.findall(r"([0-9A-Fa-f]{2}[:]){5}[0-9A-Fa-f]{2}", output)
            return macs[0].lower() if macs else None
    except Exception as e:
        print(f"Erro ao obter MAC: {e}")
        return None

def ping_panel(mac):
    while True:
        try:
            # pega IP público
            ip = requests.get("https://api.ipify.org", timeout=5).text
            # envia requisição ao painel
            r = requests.get(PAINEL_URL, params={"mac": mac, "public_ip": ip}, timeout=10)
            r.raise_for_status()
            data = r.json()
            print(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] Resposta: {data}")
        except Exception as e:
            print(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] Erro: {e}")
        time.sleep(SLEEP_INTERVAL)

if __name__ == "__main__":
    mac = get_mac()
    if not mac:
        print("Não foi possível obter o MAC. Saindo.")
        exit(1)
    print(f"MAC detectado: {mac}")
    print(f"Iniciando ping ao painel a cada {SLEEP_INTERVAL}s...")
    ping_panel(mac)
