import os
import json
import base64
import time

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException


# =========================
# CONFIG
# =========================

BASE_URL = "https://ulsolutions-org.myfreshworks.com/"
TARGET_URL = "https://ulsolutions-org.myfreshworks.com/crm/messaging/a/912274472090811/bots/bot-builder/freddy-ai-bot/6865/configure/knowledge-sources/files"

FILE_NAME = "file_mr9p2rfn49_WERCS_All_Articles.pdf"
FILE_PATH = os.path.abspath(FILE_NAME)

# =========================
# COOKIES DESDE SECRET
# =========================

cookies_base64 = os.getenv("FRESHWORKS_COOKIES")

if not cookies_base64:
    raise Exception("FRESHWORKS_COOKIES not found")

decoded = base64.b64decode(cookies_base64).decode()
cookies = json.loads(decoded)

# =========================
# DRIVER HEADLESS (ROBUSTO)
# =========================

options = Options()
options.add_argument("--disable-blink-features=AutomationControlled")
options.add_argument("--start-maximized")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--window-size=1920,1080")
options.add_argument("--disable-blink-features=AutomationControlled")

options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option("useAutomationExtension", False)

driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
  "source": """
    Object.defineProperty(navigator, 'webdriver', {
      get: () => undefined
    })
  """
})

driver = webdriver.Chrome(options=options)
wait = WebDriverWait(driver, 120)

# Anti detection básico
driver.execute_script(
    "Object.defineProperty(navigator, 'webdriver', {get: () => undefined})"
)

# =========================
# LOAD BASE
# =========================

driver.get(BASE_URL)

wait.until(
    lambda d: d.execute_script("return document.readyState") == "complete"
)

# =========================
# LOGIN VIA COOKIES
# =========================

for cookie in cookies:
    cookie.pop("sameSite", None)
    try:
        driver.add_cookie(cookie)
    except:
        pass

driver.get(TARGET_URL)

print("Esperando que la SPA termine de renderizar...")

wait.until(
    lambda d: d.execute_script(
        "return document.body && document.body.innerText.length"
    ) > 1000
)

time.sleep(5)

print("Página cargada")
print("URL actual:", driver.current_url)

driver.save_screenshot("before_interaction.png")

# =========================
# HELPER RECURSIVO IFRAMES
# =========================

def find_element_recursive(selector, context):
    elements = context.find_elements(By.CSS_SELECTOR, selector)
    if elements:
        return elements[0]

    iframes = context.find_elements(By.TAG_NAME, "iframe")

    for iframe in iframes:
        try:
            driver.switch_to.frame(iframe)
            found = find_element_recursive(selector, driver)
            if found:
                return found
            driver.switch_to.parent_frame()
        except:
            driver.switch_to.parent_frame()

    return None


def find_in_iframes(selector, timeout=120):
    end_time = time.time() + timeout

    while time.time() < end_time:
        driver.switch_to.default_content()
        found = find_element_recursive(selector, driver)
        if found:
            return found
        time.sleep(2)

    return None

# =========================
# CLICK ADD FILES
# =========================

print("Buscando botón Add files...")

add_button = find_in_iframes(
    "button[data-testid='redirect-upload--button']",
    timeout=120
)

if not add_button:
    driver.save_screenshot("debug_add_button.png")
    with open("debug_add_button.html", "w", encoding="utf-8") as f:
        f.write(driver.page_source)
    raise Exception("Add files button not found")

driver.execute_script("arguments[0].click();", add_button)
driver.switch_to.default_content()

print("Add files clicked")
time.sleep(5)

# =========================
# BUSCAR INPUT FILE DIRECTAMENTE
# =========================

print("Buscando input type=file...")

file_input = find_in_iframes(
    "input[type='file']",
    timeout=120
)

if not file_input:
    driver.save_screenshot("debug_input.png")
    with open("debug_input.html", "w", encoding="utf-8") as f:
        f.write(driver.page_source)
    raise Exception("File input not found")

print("Input encontrado, enviando archivo...")

file_input.send_keys(FILE_PATH)

time.sleep(10)

driver.save_screenshot("after_upload.png")

print("Upload enviado correctamente")

driver.quit()
