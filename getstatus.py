import requests
import time

# Diccionario de URLs con nombres descriptivos
urls = {
    'Página web - API SMG': 'https://smgapicoop.cajasmg.com/',
    'APP-Mi Caja SMG': 'https://cajanet.com/CajaAhorro/Svlt',
    'APP-Mi Cuenta SMG': 'https://app.cajasmg.com/api/v2/auth/sign-in/lookup?identification=VIHS980616HJCDRR09&identification_method=CURP',
    'APP-Mi Caja SMG': 'https://cajanet.com/CajaAhorro/Svlt',
    'Pagina Web-Atuc Entura': 'https://atuc.entura.com.mx/Login.aspx',
    'Página web - CAJANET': 'https://cajanet.com/BECSMG/',
    'Página web - CAJASMG': 'https://cajasmg.com/',
    'Pagina Web - Entura Cloud': 'https://cloud.entura.com.mx/Login.aspx',
    'Pagina Web - Entura SEL': 'https://sel.entura.com.mx/Login.aspx',
    'Pagina Web - Spei Entura': 'https://sit.entura.com.mx:8443/CloudSPEI/'
    
}


def verificar_status_http(urls: dict, intervalo: int = 10):
    while True:
        print("\n-------------------------")
        print(f"Verificación de URLs - {time.strftime('%Y-%m-%d %H:%M:%S')}")
        print("-------------------------")
        for nombre, url in urls.items():
            try:
                response = requests.get(url)
                if response.status_code == 200:
                    print(f"[OK] {nombre} está respondiendo con el código 200")
                else:
                    print(f"[ERROR] {nombre} ({url}) respondió con el código {response.status_code}")
            except requests.RequestException as e:
                print(f"[ERROR] No se pudo conectar con {nombre} ({url}). Error: {e}")
        time.sleep(intervalo)


if __name__ == '__main__':
    verificar_status_http(urls)
    #Se deja comentario de prueba 