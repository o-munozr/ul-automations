import os
import json
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait

BASE_URL = "https://ulsolutions-org.myfreshworks.com/"
TARGET_URL = "https://ulsolutions-org.myfreshworks.com/crm/messaging/a/912274472090811/bots/bot-builder/freddy-ai-bot/6865/configure/knowledge-sources/files"

cookies_json = os.getenv("FRESHWORKS_COOKIES")
cookies = json.loads(cookies_json)

options = Options()
options.add_argument("--headless=new")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--window-size=1920,1080")

driver = webdriver.Chrome(options=options)
wait = WebDriverWait(driver, 30)

# IMPORTANT: open base domain first
driver.get(BASE_URL)

for cookie in cookies:
    cookie.pop("sameSite", None)
    try:
        driver.add_cookie(cookie)
    except Exception:
        pass

# Now go directly to target
driver.get(TARGET_URL)

wait.until(lambda d: d.execute_script("return document.readyState") == "complete")

print("Logged in using cookies")

driver.quit()
