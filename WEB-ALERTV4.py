import requests
import time
import smtplib
import threading
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Configuración de las páginas a monitorear
WEBSITE_URLS = [
    "https://smgapicoop.cajasmg.com/", #Página web - API SMG
    "https://cajanet.com/CajaAhorro/Svlt", #APP - Mi Caja SMG
    "https://app.cajasmg.com/api/v2/auth/sign-in/lookup?identification=VIHS980616HJCDRR09&identification_method=CURP", #APP - Mi Cuenta SMG
    "https://atuc.entura.com.mx/Login.aspx",#Pagina Web - Atuc Entura
    "https://cajanet.com/BECSMG/", #Página web - CAJANET
    "https://cajasmg.com/", #Página web - CAJASMG
    "https://cloud.entura.com.mx/Login.aspx", #Pagina Web - Entura Cloud
    "https://sel.entura.com.mx/Login.aspx", #Pagina Web - Entura SEL
    "https://sit.entura.com.mx:8443/CloudSPEI/" #Pagina Web - Spei Entura
    
]
CHECK_INTERVAL = 50  # Intervalo de verificación en segundos
MAX_FAILURES = 3  # Número máximo de fallos consecutivos antes de enviar correo
EXPECTED_CONTENTS = {
    "https://smgapicoop.cajasmg.com/": "API SMG", #Página web - API SMG
    "https://cajanet.com/CajaAhorro/Svlt": " ", #APP - Mi Caja SMG
    "https://app.cajasmg.com/api/v2/auth/sign-in/lookup?identification=VIHS980616HJCDRR09&identification_method=CURP": "user_name", #APP - Mi Cuenta SMG
    "https://atuc.entura.com.mx/Login.aspx": "Entidad", #Pagina Web - Atuc Entura
    "https://cajanet.com/BECSMG/": "NÚMERO DE USUARIO", #Página web - CAJANET
    "https://cajasmg.com/": "Aviso de Privacidad", #Página web - CAJASMG
    "https://cloud.entura.com.mx/Login.aspx": "Autenticar", #Pagina Web - Entura Cloud
    "https://sel.entura.com.mx/Login.aspx": "Iniciar sesión", #Pagina Web - Entura SEL
    "https://sit.entura.com.mx:8443/CloudSPEI/": "Validar" #Pagina Web - Spei Entura
}

# Configuración del correo
SMTP_SERVER = 'smtp.gmail.com'
SMTP_PORT = 587
EMAIL = "jorge.hernandezhtb@gmail.com"  
PASSWORD = "yumq biyr ibxt ajli"  # Contraseña de aplicación para Gmail
RECIPIENT_EMAIL = "jorge.hernandez@ecorp.com.mx"  # Correo de destino para las alertas

def send_email(url):
    """
    Envía un correo de alerta cuando una página web no responde o no muestra el contenido esperado.
    """
    print(f"Enviando correo de alerta para {url}...")
    try:
        subject = f"Alerta: Problema con la página web {url}"
        body = (
            f"La página web en {url} no respondió correctamente "
            f"o no se encontró el contenido esperado después de {MAX_FAILURES} intentos consecutivos."
        )
        
        msg = MIMEMultipart()
        msg['From'] = EMAIL
        msg['To'] = RECIPIENT_EMAIL
        msg['Subject'] = subject
        msg.attach(MIMEText(body, 'plain'))

        # Conexión y envío del correo
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()  # Establece conexión segura
            server.login(EMAIL, PASSWORD)
            server.sendmail(EMAIL, RECIPIENT_EMAIL, msg.as_string())
            print(f"Correo enviado a {RECIPIENT_EMAIL}.")
    except Exception as e:
        print(f"Error al enviar correo: {e}")

def check_website(url, expected_text=None):
    """
    Verifica el estado de la página web.
    Si se proporciona expected_text, se valida que dicho contenido aparezca en la respuesta.
    """
    print(f"Verificando la página web {url}...")
    try:
        headers = {'User-Agent': 'Mozilla/5.0'}  # Simula un navegador
        response = requests.get(url, timeout=10, headers=headers)

        if response.status_code == 200:
            print(f"La página {url} respondió con código 200.")

            # Si se especifica contenido esperado, verificar que esté presente
            if expected_text:
                if expected_text in response.text:
                    print("El contenido esperado se encontró en la página.")
                    return True
                else:
                    print("El contenido esperado NO se encontró en la página.")
                    return False
            return True
        else:
            print(f"La página {url} devolvió el código de estado: {response.status_code}.")
            return False
    except requests.RequestException as e:
        print(f"Error al conectar con {url}: {e}")
        return False

def monitor_website(url, expected_text):
    """
    Monitorea una página web de manera independiente en un hilo.
    """
    print(f"Iniciando monitoreo para {url}...\n")
    consecutive_failures = 0  # Contador de fallos consecutivos para esta URL

    while True:
        is_website_ok = check_website(url, expected_text=expected_text)

        if is_website_ok:
            print(f"{url} está operativa.\n")
            consecutive_failures = 0  # Reiniciar contador al estar OK
        else:
            print(f"{url} está caída o sin el contenido esperado.\n")
            consecutive_failures += 1

            if consecutive_failures >= MAX_FAILURES:
                print(f"{url} ha fallado {MAX_FAILURES} veces consecutivas. Enviando alerta por correo.")
                send_email(url)
                consecutive_failures = 0  # Reiniciar contador después de la alerta

        print(f"Esperando {CHECK_INTERVAL} segundos antes de volver a verificar {url}...\n")
        time.sleep(CHECK_INTERVAL)

if __name__ == "__main__":
    # Crear un hilo para cada página a monitorear
    threads = []
    for url in WEBSITE_URLS:
        expected_text = EXPECTED_CONTENTS.get(url, None)
        thread = threading.Thread(target=monitor_website, args=(url, expected_text))
        thread.daemon = True  # Para que los hilos se cierren cuando el programa finaliza
        thread.start()
        threads.append(thread)

    # Mantener el programa corriendo indefinidamente
    for thread in threads:
        thread.join()
