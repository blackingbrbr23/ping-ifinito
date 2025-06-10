import time
import requests

URL = "https://painel-api-k2v2.onrender.com"

def manter_online():
    while True:
        try:
            response = requests.get(URL)
            print(f"[{time.ctime()}] Ping enviado - Status: {response.status_code}")
        except Exception as e:
            print(f"[{time.ctime()}] Erro ao enviar ping: {e}")
        time.sleep(5)

if __name__ == "__main__":
    manter_online()
