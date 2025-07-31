# -*- coding: utf-8 -*-
# lead_ui_test_screenshot.py

from selenium import webdriver
from selenium.webdriver.common.by import By
import pickle
import time
import os

# Edge WebDriver起動（EdgeDriverのPATHが通っている前提）
options = webdriver.EdgeOptions()
driver = webdriver.Edge(options=options)

# SalesforceインスタンスURL（自組織に合わせて固定）
BASE_URL = "https://orgfarm-89e4339fa3-dev-ed.develop.my.salesforce.com/"
LEAD_URL = f"{BASE_URL}/lightning/o/Lead/list?filterName=Recent"
COOKIE_FILE = "sf_cookies.pkl"

def load_cookies_and_open_leads():
    """Salesforceにログイン済Cookieを使ってセッションを再現"""
    driver.get(BASE_URL)
    time.sleep(3)
    if not os.path.exists(COOKIE_FILE):
        raise FileNotFoundError("❌ Cookieファイルが見つかりません。まず save_cookie.py を実行してください。")

    with open(COOKIE_FILE, "rb") as f:
        cookies = pickle.load(f)
        for cookie in cookies:
            cookie.pop("sameSite", None)
            cookie.pop("expiry", None)
            driver.add_cookie(cookie)

    driver.get(LEAD_URL)
    time.sleep(5)

def create_lead_and_capture_screenshots():
    """Leadレコードを作成し、保存前・後のスクリーンショットを取得"""
    print("▶ Lead 新規作成を開始")
    # 「新規」ボタンをクリック
    new_btn = driver.find_element(By.XPATH, '//a[@title="新規"]')
    new_btn.click()
    time.sleep(3)

    # 保存前スクリーンショット
    driver.save_screenshot("lead_before_save.png")

    # 安定XPathで各項目に入力
    driver.find_element(By.XPATH, '//label[text()="姓"]/following::input[1]').send_keys("テスト姓")
    driver.find_element(By.XPATH, '//label[text()="会社"]/following::input[1]').send_keys("テスト会社")

    # 保存ボタンをクリック
    save_btn = driver.find_element(By.XPATH, '//button[@name="SaveEdit"]')
    save_btn.click()

    # 保存完了を待機
    time.sleep(6)

    # 保存後スクリーンショット
    driver.save_screenshot("lead_after_save.png")
    print("✅ スクリーンショット完了：lead_before_save.png / lead_after_save.png")

try:
    load_cookies_and_open_leads()
    create_lead_and_capture_screenshots()
    print("✅ UIテスト完了")
finally:
    driver.quit()
