import os
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options

BASE_URL = "https://ulsolutions-org.myfreshworks.com/"
TARGET_URL = "https://ulsolutions-org.myfreshworks.com/crm/messaging/a/912274472090811/bots/bot-builder/freddy-ai-bot/6865/configure/knowledge-sources/files"

EMAIL = os.getenv("FRESHWORKS_EMAIL")
PASSWORD = os.getenv("FRESHWORKS_PASSWORD")

FILE_PATH = "file_mr9p2rfn49_WERCS_All_Articles.pdf"  # El archivo debe estar en el repo

options = Options()
options.add_argument("--headless=new")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--window-size=1920,1080")

driver = webdriver.Chrome(options=options)
wait = WebDriverWait(driver, 40)

# -------------------
# LOGIN
# -------------------

driver.get(BASE_URL)

email_input = wait.until(
    EC.presence_of_element_located((By.XPATH, "//input[@type='email']"))
)
email_input.send_keys(EMAIL)

try:
    driver.find_element(By.XPATH, "//button[contains(., 'Next')]").click()
except:
    pass

password_input = wait.until(
    EC.presence_of_element_located((By.XPATH, "//input[@type='password']"))
)
password_input.send_keys(PASSWORD)

driver.find_element(By.XPATH, "//button[contains(., 'Sign') or contains(., 'Login')]").click()

wait.until(lambda d: d.execute_script("return document.readyState") == "complete")

print("Login successful")

# -------------------
# GO TO TARGET
# -------------------

driver.get(TARGET_URL)
wait.until(lambda d: d.execute_script("return document.readyState") == "complete")

print("Navigation complete")

driver.quit()
