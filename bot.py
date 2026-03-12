import sys
print("Python version:", sys.version)

from flask import Flask, request
import os

app = Flask(__name__)

VERIFY_TOKEN = "binance_token"

@app.route("/")
def home():
    return "Bot Binance activo"

@app.route("/webhook", methods=["GET"])
def verify_webhook():
    token = request.args.get("hub.verify_token")
    challenge = request.args.get("hub.challenge")
    if token == VERIFY_TOKEN:
        return challenge
    return "Verification token mismatch", 403

@app.route("/webhook", methods=["POST"])
def recibir_mensaje():
    data = request.json
    print("Mensaje recibido:", data)
    return "ok", 200

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)