# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver.edge.service import Service
from selenium.webdriver.common.by import By
import pickle
import time
import os

# Edge WebDriver起動
service = Service(executable_path="C:/WebDriver/MicrosoftEdgeDeveloper/msedgedriver.exe")
driver = webdriver.Edge(service=service)

# SalesforceインスタンスURL
BASE_URL = "https://orgfarm-89e4339fa3-dev-ed.develop.my.salesforce.com/"
LEAD_URL = f"{BASE_URL}/lightning/o/Lead/list?filterName=Recent"
COOKIE_FILE = "sf_cookies.pkl"

def load_cookies_and_open_leads():
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
    print("▶ Lead 新規作成を開始")
    # 「新規」ボタンをクリック
    driver.find_element(By.XPATH, '//a[@title="新規"]').click()
    time.sleep(3)

    # スクリーンショット（保存前）
    driver.save_screenshot("lead_before_save.png")

    # テキスト項目
    driver.find_element(By.XPATH, '//label[text()="姓"]/following::input[1]').send_keys("自動生成姓")
    driver.find_element(By.XPATH, '//label[text()="会社"]/following::input[1]').send_keys("自動生成会社")

    # 選択リスト：「最終変更種別」
    driver.find_element(By.XPATH, '//label[text()="最終変更種別"]/following::div//button').click()
    time.sleep(1)
    driver.find_element(By.XPATH, '//span[@title="本人からの依頼"]').click()

    # 複数選択リスト：「商品リスト」
    driver.find_element(By.XPATH, '//label[text()="商品リスト"]/following::div//button').click()
    time.sleep(1)
    driver.find_element(By.XPATH, '//span[@title="IT"]').click()
    driver.find_element(By.XPATH, '//span[@title="Jordan"]').click()

    # 選択リスト：「リード 状況」
    driver.find_element(By.XPATH, '//label[text()="リード 状況"]/following::div//button').click()
    time.sleep(1)
    driver.find_element(By.XPATH, '//span[@title="Working - Contacted"]').click()

    # 参照関係：「関連キャンペーン」
    lookup = driver.find_element(By.XPATH, '//input[@title="キャンペーンを検索"]')
    lookup.send_keys("DM Campaign to Top Customers - Nov 12-23, 2001")
    time.sleep(2)
    driver.find_element(By.XPATH, '//lightning-base-combobox-formatted-text').click()

    # 保存ボタン
    driver.find_element(By.XPATH, '//button[@name="SaveEdit"]').click()
    time.sleep(6)

    # スクリーンショット（保存後）
    driver.save_screenshot("lead_after_save.png")
    print("✅ 完了：lead_before_save.png / lead_after_save.png")

try:
    load_cookies_and_open_leads()
    create_lead_and_capture_screenshots()
    print("✅ UI登録テスト完了")
finally:
    driver.quit()
