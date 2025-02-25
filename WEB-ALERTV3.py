import requests
import time
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Configuración
WEBSITE_URL = "https://smgapicoop.cajasmg.com/"
CHECK_INTERVAL = 10  # Intervalo de verificación en segundos
MAX_FAILURES = 3  # Número máximo de fallos consecutivos antes de enviar correo

# Configuración del correo
SMTP_SERVER = 'smtp.gmail.com'
SMTP_PORT = 587
EMAIL = "jorge.hernandezhtb@gmail.com"  
PASSWORD = "yumq biyr ibxt ajli"  # Contraseña de aplicación para Gmail
RECIPIENT_EMAIL = "jorge.hernandez@ecorp.com.mx"  # Correo de destino para las alertas

def send_email(url):
    """
    Envía un correo de alerta cuando la página web no responde o no muestra el contenido esperado.
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

def main():
    """
    Bucle principal del script. Monitorea la página web continuamente
    y envía una alerta si detecta que está caída varias veces consecutivas.
    """
    print("Iniciando monitoreo de la página web...\n")
    consecutive_failures = 0  # Contador de fallos consecutivos

    while True:
        is_website_ok = check_website(WEBSITE_URL, expected_text=EXPECTED_CONTENT)

        if is_website_ok:
            print("Estado: Página web operativa.\n")
            consecutive_failures = 0  # Reiniciar contador al estar OK
        else:
            print("Estado: Página web caída o sin el contenido esperado.\n")
            consecutive_failures += 1

            if consecutive_failures >= MAX_FAILURES:
                print(f"La página ha fallado {MAX_FAILURES} veces consecutivas. Enviando alerta por correo.")
                send_email(WEBSITE_URL)
                consecutive_failures = 0  # Reiniciar contador después de la alerta

        print(f"Esperando {CHECK_INTERVAL} segundos para la próxima verificación...\n")
        time.sleep(CHECK_INTERVAL)

if __name__ == "__main__":
    main()
