import os
import json
import base64

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
