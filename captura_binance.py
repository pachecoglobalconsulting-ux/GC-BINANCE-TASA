from playwright.sync_api import sync_playwright
from PIL import Image

# ===============================
# Configuración
# ===============================
url = "https://p2p.binance.com/en/trade/sell/USDT?fiat=VES"
# Ajusta la caja según la resolución de tu navegador y el área de los anuncios
# (left, top, right, bottom)
caja_recorte = (0, 300, 1920, 1500)  # ejemplo: recorta la zona donde aparecen los primeros 4 anuncios

# ===============================
# Ejecutar Playwright
# ===============================
with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)  # False para depuración; True si quieres sin ver navegador
    page = browser.new_page()
    page.goto(url)

    # esperar a que cargue JavaScript
    page.wait_for_timeout(8000)  # 8 segundos; ajustar si la página es lenta

    # screenshot completo de la página
    page.screenshot(path="pagina_completa.png", full_page=True)

    browser.close()

# ===============================
# Recortar la zona de los primeros 4 anuncios
# ===============================
imagen = Image.open("pagina_completa.png")
imagen_recortada = imagen.crop(caja_recorte)
imagen_recortada.save("precio.png")

print("Captura de los primeros 4 anuncios creada: precio.png")