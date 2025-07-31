# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver.edge.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import json
import time

# EdgeドライバパスとURL
DRIVER_PATH = "C:/WebDriver/MicrosoftEdgeDeveloper/msedgedriver.exe"
BASE_URL = "https://orgfarm-89e4339fa3-dev-ed.develop.my.salesforce.com"
LEAD_URL = f"{BASE_URL}/lightning/o/Lead/list?filterName=Recent"
COOKIE_FILE = "manual_cookies.json"

# ドライバ起動
service = Service(executable_path=DRIVER_PATH)
options = webdriver.EdgeOptions()
driver = webdriver.Edge(service=service, options=options)
wait = WebDriverWait(driver, 15)

def load_manual_cookies():
    driver.get(BASE_URL)  # cookieをセットする前に同一ドメインへアクセス
    with open(COOKIE_FILE, "r", encoding="utf-8") as f:
        cookies = json.load(f)
        for cookie in cookies:
            cookie.pop("expiry", None)
            cookie.pop("sameSite", None)
            driver.add_cookie(cookie)
    print("✅ Cookie 読み込み完了")

def open_lead_list():
    driver.get(LEAD_URL)
    wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="brandBand_1"]')))
    print("✅ リード一覧画面の読み込み完了")

def create_lead_and_capture_screenshots():
    print("▶ Lead 新規作成を開始")

    # 新規ボタン（固定XPath or 安定ラベル使用）
    wait.until(EC.element_to_be_clickable((By.XPATH, '//a[@title="新規"]'))).click()
    time.sleep(5)
    driver.save_screenshot("lead_before_save.png")

    # テキスト入力
    wait.until(EC.presence_of_element_located((By.XPATH, '//label[text()="姓"]/following::input[1]'))).send_keys("自動生成姓")
    wait.until(EC.presence_of_element_located((By.XPATH, '//label[text()="会社名"]/following::input[1]'))).send_keys("自動生成会社")

    # 最終変更種別（選択リスト）
    dropdown = wait.until(EC.element_to_be_clickable((By.XPATH, '//label[text()="最終変更種別"]/following::div//button')))
    driver.execute_script("arguments[0].click();", dropdown)
    wait.until(EC.element_to_be_clickable((By.XPATH, '//span[@title="本人からの依頼"]'))).click()

    # 商品リスト（複数選択リスト）
    driver.execute_script("arguments[0].scrollIntoView();", driver.find_element(By.XPATH, '//div[text()="商品リスト"]'))
    wait.until(EC.element_to_be_clickable((By.XPATH, '//span[@title="IT"]/ancestor::div[@role="option"]'))).click()
    wait.until(EC.element_to_be_clickable((By.XPATH, '//span[@title="Jordan"]/ancestor::div[@role="option"]'))).click()

    # リード状況（選択リスト）
    dropdown = wait.until(EC.element_to_be_clickable((By.XPATH, '//label[text()="リード 状況"]/following::div//button')))
    driver.execute_script("arguments[0].click();", dropdown)
    wait.until(EC.element_to_be_clickable((By.XPATH, '//span[@title="Working - Contacted"]'))).click()

    # 関連キャンペーン（参照関係）
    lookup = wait.until(EC.presence_of_element_located((By.XPATH, '//input[@title="キャンペーンを検索"]')))
    lookup.send_keys("DM Campaign to Top Customers")
    time.sleep(2)
    wait.until(EC.element_to_be_clickable((By.XPATH, '//lightning-base-combobox-formatted-text'))).click()

    # 保存
    wait.until(EC.element_to_be_clickable((By.XPATH, '//button[@name="SaveEdit"]'))).click()
    time.sleep(5)
    driver.save_screenshot("lead_after_save.png")
    print("✅ スクリーンショット取得完了：lead_before_save.png / lead_after_save.png")

# 実行
try:
    load_manual_cookies()
    open_lead_list()
    create_lead_and_capture_screenshots()
    print("✅ リード新規作成テスト完了")
finally:
    driver.quit()
