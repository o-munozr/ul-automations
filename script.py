import os
import json
import base64
import time
import pickle

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait



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
# DRIVER HEADLESS
# =========================

options = Options()
options.binary_location = "/usr/bin/google-chrome"

options.add_argument("--headless=new")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--disable-gpu")
options.add_argument("--window-size=1920,1080")
options.add_argument("--remote-debugging-port=9222")

driver = webdriver.Chrome(options=options)

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
    except Exception:
        pass

driver.get(TARGET_URL)

wait.until(
    lambda d: d.execute_script("return document.readyState") == "complete"
)

print("Esperando iframes...")

wait.until(
    lambda d: len(d.find_elements(By.TAG_NAME, "iframe")) > 0
)

print("Iframes detectados:", len(driver.find_elements(By.TAG_NAME, "iframe")))
time.sleep(5)

# =========================
# HELPER: FIND IN IFRAMES
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


def find_in_iframes(selector, timeout=60):
    end_time = time.time() + timeout

    while time.time() < end_time:
        driver.switch_to.default_content()
        print("Buscando input en estructura completa de iframes...")
        found = find_element_recursive(selector, driver)
        if found:
            return found
        time.sleep(2)

    return None

# =========================
# CLICK ADD FILES
# =========================

print("Buscando botón Add files...")

add_files_button = find_in_iframes(
    "button[data-testid='redirect-upload--button']",
    timeout=60
)

if not add_files_button:
    raise Exception("Add files button not found")

driver.execute_script("arguments[0].click();", add_files_button)
driver.switch_to.default_content()

print("Add files button clicked")

time.sleep(3)

# =========================
# CLICK UPLOAD FILE
# =========================

print("Buscando botón Upload File...")

upload_file_button = find_in_iframes(
    "button",
    timeout=60
)

if not upload_file_button:
    raise Exception("Upload File button not found")

driver.execute_script("arguments[0].click();", upload_file_button)
driver.switch_to.default_content()

print("Upload File button clicked")

time.sleep(5)

# =========================
# SEND FILE
# =========================

print("Buscando input file...")

file_input = find_in_iframes(
    "input[data-testid='listAction-file--input']",
    timeout=60
)

if not file_input:
    raise Exception("File input not found")

file_input.send_keys(FILE_PATH)

print("File uploaded")
