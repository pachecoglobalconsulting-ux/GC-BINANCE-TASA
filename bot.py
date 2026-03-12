from flask import Flask, request
import os
import requests
import subprocess
from datetime import datetime

app = Flask(__name__)

VERIFY_TOKEN = "binance_token"

# ===============================
# Verificación del webhook
# ===============================
@app.route("/webhook", methods=["GET"])
def verify_webhook():
    token = request.args.get("hub.verify_token")
    challenge = request.args.get("hub.challenge")

    if token == VERIFY_TOKEN:
        return challenge
    return "Verification token mismatch", 403


# ===============================
# Recibir mensajes de WhatsApp
# ===============================
@app.route("/webhook", methods=["POST"])
def recibir_mensaje():
    data = request.json
    print("Mensaje recibido:", data)
    return "ok", 200


# ===============================
# Ejecutar captura_binance.py
# ===============================
def generar_captura():
    subprocess.run(["python3", "captura_binance.py"])


# ===============================
# Obtener tasa Binance
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

    for ad in data["data"]:
        price = float(ad["adv"]["price"])
        available = float(ad["adv"]["surplusAmount"])
        methods = ad["adv"]["tradeMethods"]

        if available < 20000:
            continue

        metodo_valido = False

        for m in methods:
            metodo = m["tradeMethodName"].lower()

            for permitido in metodos_permitidos:
                if permitido in metodo:
                    metodo_valido = True
                    break

        if metodo_valido:
            return price

    return None


# ===============================
# Generar mensaje
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
# WhatsApp Cloud API
# ===============================
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
            "link": f"https://TU_SERVIDOR.com/{imagen}",
            "caption": caption
        }
    }

    requests.post(url, headers=headers, json=data)


# ===============================
# Servidor Railway
# ===============================
if __name__ == "__main__":

    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)