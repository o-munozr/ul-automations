import os
import json
import base64
import time

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


# =========================
# CONFIG
# =========================

BASE_URL = "https://ulsolutions-org.myfreshworks.com/"
TARGET_URL = "https://ulsolutions-org.myfreshworks.com/crm/messaging/a/912274472090811/bots/bot-builder/freddy-ai-bot/6865/configure/knowledge-sources/files"

FILE_NAME = "file_mr9p2rfn49_WERCS_All_Articles.pdf"
FILE_PATH = os.path.abspath(FILE_NAME)

if not os.path.exists(FILE_PATH):
    raise Exception(f"File not found: {FILE_PATH}")

# =========================
# COOKIES DESDE SECRET
# =========================

cookies_base64 = os.getenv("FRESHWORKS_COOKIES")

if not cookies_base64:
    raise Exception("FRESHWORKS_COOKIES not found")

decoded = base64.b64decode(cookies_base64).decode()
cookies = json.loads(decoded)

# =========================
# DRIVER HEADLESS
# =========================

options = Options()
options.add_argument("--headless=new")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--window-size=1920,1080")

driver = webdriver.Chrome(options=options)
wait = WebDriverWait(driver, 60)

# =========================
# LOGIN VIA COOKIES
# =========================

driver.get(BASE_URL)

wait.until(lambda d: d.execute_script("return document.readyState") == "complete")

for cookie in cookies:
    cookie.pop("sameSite", None)
    try:
        driver.add_cookie(cookie)
    except Exception:
        pass

driver.get(TARGET_URL)

wait.until(lambda d: d.execute_script("return document.readyState") == "complete")

print("Página cargada")

# =========================
# CLICK ADD FILES
# =========================

print("Buscando botón Add files...")

add_button = wait.until(
    EC.presence_of_element_located(
        (By.CSS_SELECTOR, "button[data-testid='redirect-upload--button']")
    )
)

driver.execute_script("arguments[0].click();", add_button)

print("Add files clicked")

# =========================
# ESPERAR INPUT DIRECTAMENTE
# =========================

print("Esperando input file...")

file_input = wait.until(
    EC.presence_of_element_located(
        (By.CSS_SELECTOR, "input[data-testid='listAction-file--input']")
    )
)

print("Input detectado, subiendo archivo...")

file_input.send_keys(FILE_PATH)

# =========================
# ESPERAR REDIRECT AUTOMÁTICO
# =========================

print("Esperando redirección automática...")

wait.until(lambda d: "bots" in d.current_url)

print("Redirección detectada")
print("URL actual:", driver.current_url)

time.sleep(5)
driver.quit()
