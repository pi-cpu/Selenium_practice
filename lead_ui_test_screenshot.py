
from selenium import webdriver
from selenium.webdriver.common.by import By
import pickle
import time

# Edge WebDriver起動
options = webdriver.EdgeOptions()
driver = webdriver.Edge(options=options)

# SalesforceインスタンスURL（必要に応じて変更）
BASE_URL = "https://orgfarm-89e4339fa3-dev-ed.develop.my.salesforce.com/"
LEAD_URL = f"{BASE_URL}/lightning/o/Lead/list?filterName=Recent"

# Cookieファイルパス
COOKIE_FILE = "sf_cookies.pkl"

def load_cookies_and_open_leads():
    driver.get(BASE_URL)
    time.sleep(3)
    with open(COOKIE_FILE, "rb") as f:
        cookies = pickle.load(f)
        for cookie in cookies:
            cookie.pop("sameSite", None)
            cookie.pop("expiry", None)
            driver.add_cookie(cookie)
    driver.get(LEAD_URL)
    time.sleep(5)

def create_lead_and_capture_screenshots():
    driver.find_element(By.XPATH, '//a[@title="新規"]').click()
    time.sleep(3)
    driver.save_screenshot("lead_before_save.png")

    driver.find_element(By.XPATH, '//label[text()="姓"]/following::input[1]').send_keys("テスト姓")
    driver.find_element(By.XPATH, '//label[text()="会社"]/following::input[1]').send_keys("テスト会社")

    driver.find_element(By.XPATH, '//button[@name="SaveEdit"]').click()
    time.sleep(6)
    driver.save_screenshot("lead_after_save.png")

try:
    load_cookies_and_open_leads()
    create_lead_and_capture_screenshots()
    print("✅ UIテスト完了：スクリーンショット取得済み")
finally:
    driver.quit()
