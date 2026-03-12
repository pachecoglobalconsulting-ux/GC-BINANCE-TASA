# captura_binance.py
from playwright.sync_api import sync_playwright
from PIL import Image
import time

def capturar_binance():
    url = "https://p2p.binance.com/en/trade/sell/USDT?fiat=VES"

    # Inicia Playwright y abre la página
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto(url)

        # Esperar que cargue la página (ajustable)
        page.wait_for_timeout(5000)

        # Tomar screenshot completo
        page.screenshot(path="full_precio.png", full_page=True)
        browser.close()

    # Abrir la imagen completa y recortar solo los primeros 5 anuncios
    # Ajusta estas coordenadas según la resolución y tu página
    try:
        img = Image.open("full_precio.png")

        # Por ejemplo, recortamos desde la parte superior, ancho completo, alto de ~500px (ajusta si necesitas)
        left = 0
        top = 0
        right = img.width
        bottom = 500  # alto aproximado de 5 anuncios

        img_cropped = img.crop((left, top, right, bottom))
        img_cropped.save("precio.png")
        print("Captura recortada creada: precio.png")
    except Exception as e:
        print("Error al recortar la imagen:", e)

# ===============================
# Bloque principal
# ===============================
if __name__ == "__main__":
    capturar_binance()