from flask import Flask, request
import os

import requests
import subprocess
from datetime import datetime

app = Flask(__name__)

VERIFY_TOKEN = "binance_token"

@app.route("/webhook", methods=["GET"])
def verify_webhook():
    token = request.args.get("hub.verify_token")
    challenge = request.args.get("hub.challenge")

    if token == VERIFY_TOKEN:
        return challenge
    return "Verification token mismatch", 403
# ===============================
# 1️⃣ Función para ejecutar captura_binance.py
# ===============================
def generar_captura():
    subprocess.run(["python3", "captura_binance.py"])

# ===============================
# 2️⃣ Función para obtener la tasa filtrada de Binance
# ===============================
def obtener_tasa_binance():
    url = "https://p2p.binance.com/bapi/c2c/v2/friendly/c2c/adv/search"
    payload = {
        "page": 1,
        "rows": 20,
        "asset": "USDT",
        "fiat": "VES",
        "tradeType": "SELL"
    }

    response = requests.post(url, json=payload)
    data = response.json()

    metodos_permitidos = ["bank transfer", "pago móvil", "banesco", "mercantil", "bnc"]
    precio_final = None

    for ad in data["data"]:
        price = float(ad["adv"]["price"])
        available = float(ad["adv"]["surplusAmount"])
        methods = ad["adv"]["tradeMethods"]

        # verificar liquidez mínima
        if available < 20000:
            continue

        # verificar métodos permitidos
        metodo_valido = False
        for m in methods:
            metodo = m["tradeMethodName"].lower()
            for permitido in metodos_permitidos:
                if permitido in metodo:
                    metodo_valido = True
                    break

        if metodo_valido:
            precio_final = price
            break

    return precio_final

# ===============================
# 3️⃣ Función para generar mensaje profesional
# ===============================
def generar_mensaje(tasa):
    ahora = datetime.now()
    hora = ahora.strftime("%H:%M")
    fecha = ahora.strftime("%d/%m/%Y")

    mensaje = f"""
📊 Tasa de referencia Binance P2P

La tasa actual filtrada en Binance es:

💰 {tasa} Bs por USDT

Actualizada a las {hora} del día {fecha}.

Por favor consulte la imagen adjunta para verificación de la tasa correspondiente.
"""
    return mensaje

# ===============================
# 4️⃣ Función para enviar imagen por WhatsApp Cloud API
# ===============================
import os
import requests

ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")
PHONE_NUMBER_ID = os.getenv("PHONE_NUMBER_ID")

def enviar_imagen_whatsapp(numero, imagen, caption):
    url = f"https://graph.facebook.com/v18.0/{PHONE_NUMBER_ID}/messages"
    headers = {
        "Authorization": f"Bearer {ACCESS_TOKEN}",
        "Content-Type": "application/json"
    }
    data = {
        "messaging_product": "whatsapp",
        "to": numero,
        "type": "image",
        "image": {
            "link": f"https://TU_SERVIDOR.com/{imagen}",  # URL pública
            "caption": caption
        }
    }
    requests.post(url, headers=headers, json=data)

# ===============================
# 5️⃣ Simulación de comando /tasa
# ===============================
if __name__ == "__main__":
    mensaje_usuario = "/tasa"
    telefono_usuario = "584226865055"  # tu número de prueba

    if mensaje_usuario.lower() == "/tasa":
        print("Recibiendo comando /tasa…")
        generar_captura()  # genera precio.png
        tasa = obtener_tasa_binance()  # obtiene la tasa filtrada
        if tasa is None:
            print("No se encontró ningún anuncio válido.")
        else:
            texto = generar_mensaje(tasa)
            print(texto)  # muestra mensaje en consola para prueba
            # enviar_imagen_whatsapp(telefono_usuario, "precio.png", texto)  # descomenta cuando tengas URL pública
