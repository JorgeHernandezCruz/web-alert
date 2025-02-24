import requests
import time

def check_website(url, max_attempts=3, interval=10):
    while True:
        attempts = 0
        while attempts < max_attempts:
            try:
                response = requests.get(url, timeout=5)
                if response.status_code == 200:
                    print(f"La página {url} está activa (Status 200).")
                    break
                else:
                    print(f"La página {url} respondió con estado {response.status_code}.")
            except requests.RequestException as e:
                print(f"Error al acceder a {url}: {e}")
            
            attempts += 1
            print(f"Intento {attempts} de {max_attempts}. Reintentando en {interval} segundos...")
            time.sleep(interval)
        
        if attempts == max_attempts:
            print(f"La página {url} está inactiva después de {max_attempts} intentos.")
        
        print("Reiniciando monitoreo en 10 segundos...")
        time.sleep(10)

if __name__ == "__main__":
    website_url = "https://smgapicoop.cajasmg.com/"
    check_website(website_url)