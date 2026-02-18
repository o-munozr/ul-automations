import os
import json
import base64
import time

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


BASE_URL = "https://ulsolutions-org.myfreshworks.com/"
TARGET_URL = "https://ulsolutions-org.myfreshworks.com/crm/messaging/a/912274472090811/bots/bot-builder/freddy-ai-bot/6865/configure/knowledge-sources/files"

FILE_NAME = "file_mr9p2rfn49_WERCS_All_Articles.pdf"
FILE_PATH = os.path.abspath(FILE_NAME)


cookies_base64 = os.getenv("FRESHWORKS_COOKIES")

if not cookies_base64:
    raise Exception("FRESHWORKS_COOKIES not found")

decoded = base64.b64decode(cookies_base64).decode()
cookies = json.loads(decoded)


options = Options()
options.add_argument("--headless=new")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--window-size=1920,1080")

driver = webdriver.Chrome(options=options)
wait = WebDriverWait(driver, 60)



driver.get(BASE_URL)
wait.until(lambda d: d.execute_script("return document.readyState") == "complete")

for cookie in cookies:
    cookie.pop("sameSite", None)
    try:
        driver.add_cookie(cookie)
    except Exception as e:
        print("Cookie error:", e)

driver.get(TARGET_URL)

wait.until(lambda d: d.execute_script("return document.readyState") == "complete")

# Validar sesión
if "login" in driver.current_url.lower():
    raise Exception("Sesión inválida - redirigido a login")

print("✅ Sesión iniciada correctamente")



def find_in_iframes(selector, timeout=60):
    start = time.time()
    while time.time() - start < timeout:
        driver.switch_to.default_content()
        iframes = driver.find_elements(By.TAG_NAME, "iframe")

        for iframe in iframes:
            try:
                driver.switch_to.frame(iframe)
                elements = driver.find_elements(By.CSS_SELECTOR, selector)
                if elements:
                    return elements[0]
                driver.switch_to.default_content()
            except Exception:
                driver.switch_to.default_content()

        time.sleep(1)

    return None



add_files_button = find_in_iframes(
    "button[data-testid='upload-source-button']",
    timeout=60
)

if not add_files_button:
    raise Exception("Add files button not found")

driver.execute_script("arguments[0].click();", add_files_button)
driver.switch_to.default_content()

print("📁 Add files button clicked")



upload_file_button = find_in_iframes(
    "button",
    timeout=60
)

if not upload_file_button:
    raise Exception("Upload File button not found")

driver.execute_script("arguments[0].click();", upload_file_button)
driver.switch_to.default_content()

print("⬆ Upload File button clicked")


file_input = find_in_iframes(
    "input[type='file']",
    timeout=60
)

if not file_input:
    raise Exception("File input not found")

file_input.send_keys(FILE_PATH)

print("✅ Archivo enviado:", FILE_PATH)



time.sleep(20)

print("🎉 Proceso terminado correctamente")

driver.quit()
