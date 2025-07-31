# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver.edge.service import Service
from selenium.webdriver.edge.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
import time
import json

# --- 設定 ---
COOKIE_FILE = "manual_cookies.json"  # あなたが用意したクッキーファイル名
BASE_URL = "https://orgfarm-89e4339fa3-dev-ed.develop.my.salesforce.com"
LEAD_URL = f"{BASE_URL}/lightning/o/Lead/list?filterName=Recent"

# --- ドライバー準備 ---
options = Options()
service = Service(executable_path="C:/WebDriver/MicrosoftEdgeDeveloper/msedgedriver.exe")
driver = webdriver.Edge(service=service, options=options)
wait = WebDriverWait(driver, 20)

def load_cookies_and_open_leads():
    driver.get(BASE_URL)
    time.sleep(3)

    with open(COOKIE_FILE, "r", encoding="utf-8") as f:
        cookies = json.load(f)
        for cookie in cookies:
            cookie["sameSite"] = 'Strict'
            if "expiry" in cookie:
                del cookie["expiry"]
            driver.add_cookie(cookie)

    driver.get(LEAD_URL)
    wait.until(EC.presence_of_element_located((By.XPATH, '//a[@title="新規"]')))
    print("✅ リード一覧画面の読み込み完了")

def create_lead_and_capture_screenshots():
    print("▶ Lead 新規作成を開始")
    driver.find_element(By.XPATH, '//a[@title="新規"]').click()
    time.sleep(3)
    driver.save_screenshot("lead_before_save.png")

    # テキスト
    # テキスト
    wait.until(EC.presence_of_element_located((By.XPATH, '//label[text()="姓"]/following::input[1]'))).send_keys("自動生成姓1")
    driver.find_element(By.XPATH, '//label[text()="会社名"]/following::input[1]').send_keys("自動生成会社1")

    # 選択リスト：最終変更種別
    # 選択リスト：最終変更種別
    button = wait.until(EC.presence_of_element_located((By.XPATH, '//label[text()="最終変更種別"]/following::button[1]')))
    driver.execute_script("arguments[0].scrollIntoView(true);", button)
    time.sleep(1)
    driver.execute_script("arguments[0].click();", button)

    option = wait.until(EC.element_to_be_clickable((By.XPATH, '//span[@title="本人からの依頼"]')))
    driver.execute_script("arguments[0].click();", option)


    # 商品リスト（複数選択）
    def select_dual_listbox_items(labels):
        for label in labels:
            option_xpath = f'//span[@title="{label}"]/ancestor::div[@role="option"]'
            option_element = wait.until(EC.element_to_be_clickable((By.XPATH, option_xpath)))
            driver.execute_script("arguments[0].click();", option_element)
            time.sleep(0.5)  # 一呼吸置くと安定しやすい

            move_button = wait.until(EC.element_to_be_clickable((By.XPATH, '//button[@title="選択済み に移動"]')))
            driver.execute_script("arguments[0].click();", move_button)
            print(f"✅ 商品リストに {labels} を追加")

    # 呼び出し
    select_dual_listbox_items(["IT", "Jordan"])


    # 選択リスト：「リード 状況」
    lead_status_button = wait.until(EC.presence_of_element_located((By.XPATH, '//label[text()="リード 状況"]/following::button[1]')))
    driver.execute_script("arguments[0].scrollIntoView(true);", lead_status_button)
    time.sleep(0.5)
    driver.execute_script("arguments[0].click();", lead_status_button)

    # 選択肢「Working - Contacted」を選択
    lead_status_option = wait.until(EC.element_to_be_clickable((By.XPATH, '//span[@title="Working - Contacted"]/ancestor::lightning-base-combobox-item')))
    driver.execute_script("arguments[0].scrollIntoView(true);", lead_status_option)
    time.sleep(0.5)
    driver.execute_script("arguments[0].click();", lead_status_option)


    # 参照関係：「関連キャンペーン」
    lookup = wait.until(EC.presence_of_element_located((By.XPATH, '//input[@placeholder="キャンペーンを検索..."]')))
    lookup.send_keys("DM Campaign to Top Customers - Nov 12-23, 2001")
    time.sleep(2)
    driver.execute_script("arguments[0].click();", wait.until(EC.element_to_be_clickable((By.XPATH, '//lightning-base-combobox-formatted-text'))))

    # 保存
    wait.until(EC.element_to_be_clickable((By.XPATH, '//button[@name="SaveEdit"]'))).click()
    time.sleep(5)
    driver.save_screenshot("lead_after_save.png")
    print("✅ UIテスト完了（スクリーンショット保存）")

# --- 実行 ---
try:
    load_cookies_and_open_leads()
    create_lead_and_capture_screenshots()
finally:
    driver.quit()
