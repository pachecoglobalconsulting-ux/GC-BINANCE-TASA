# captura_binance.py
from playwright.sync_api import sync_playwright
from PIL import Image

def capturar_binance():
    url = "https://p2p.binance.com/en/trade/sell/USDT?fiat=VES"

    # Playwright abre la página
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto(url)
        page.wait_for_timeout(5000)
        page.screenshot(path="full_precio.png", full_page=True)
        browser.close()

    # Recortar solo primeros 5 anuncios
    try:
        img = Image.open("full_precio.png")
        left = 0
        top = 0
        right = img.width
        bottom = 500  # Ajusta según la altura de 5 anuncios
        img_cropped = img.crop((left, top, right, bottom))
        img_cropped.save("precio.png")
        print("Captura recortada creada: precio.png")
    except Exception as e:
        print("Error al recortar la imagen:", e)

if __name__ == "__main__":
    capturar_binance()