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
COOKIE_FILE = "manual_cookies.json"  # あなたが用意したクッキーファイル名
BASE_URL = "https://cybernet--takahara.sandbox.my.salesforce.com/"
LEAD_URL = f"{BASE_URL}/lightning/o/Lead/list?filterName=RecentlyViewedLeads"

# --- ドライバー準備 ---
options = Options()
options.add_argument("--disable-notifications")

import os
edge_driver_path = r"C:/WebDriver/MicrosoftEdgeDeveloper/msedgedriver.exe"
service = Service(executable_path=edge_driver_path)
driver = webdriver.Edge(service=service, options=options)
wait = WebDriverWait(driver, 20)

def load_cookies_and_open_leads():
    driver.get(BASE_URL)
    time.sleep(3)
    with open(COOKIE_FILE, "r", encoding="utf-8") as f:
        cookies = json.load(f)
        for cookie in cookies:
            cookie.pop("expiry", None)
            cookie["sameSite"] = cookie.get("sameSite") or "None"
            cookie["secure"] = True
            cookie.setdefault("domain", ".my.salesforce.com")
            try:
                driver.add_cookie(cookie)
            except Exception as e:
                print(f"Warning: failed to add cookie {cookie.get('name')}: {e}")
    driver.get(LEAD_URL)
    wait.until(EC.presence_of_element_located((By.XPATH, '//a[@title="新規"]')))
    print("✅ リード一覧画面の読み込み完了")

def create_lead_and_capture_screenshots():
    print("▶ Lead 新規作成を開始")
    new_button = wait.until(EC.element_to_be_clickable((By.XPATH, '//a[@title="新規"]')))
    new_button.click()
    driver.save_screenshot("lead_before_save.png")

    # ラジオボタン
    radio_button = wait.until(EC.presence_of_element_located((By.XPATH, '//span[contains(text(), "項目A")]/ancestor::label')))
    driver.execute_script("arguments[0].scrollIntoView(true);", radio_button)
    driver.execute_script("arguments[0].click();", radio_button)
    wait.until(EC.element_to_be_clickable((By.XPATH, '//button[.//span[text()="次へ"]]'))).click()
    wait.until(EC.presence_of_element_located((By.XPATH, '//label[text()="項目B"]/following::input[1]')))

    # 入力フィールドの操作
    last_name = wait.until(EC.element_to_be_clickable((By.XPATH, '//label[text()="項目B"]/following::input[1]')))
    last_name.send_keys("自動生成項目B")
    company_name = wait.until(EC.element_to_be_clickable((By.XPATH, '//label[text()="項目C"]/following::input[1]')))
    company_name.send_keys("自動生成項目C")

    # 選択リスト：項目D
    field_button = wait.until(EC.element_to_be_clickable((By.XPATH, '//label[text()="項目D"]/following::button[1]')))
    driver.execute_script("arguments[0].scrollIntoView(true);", field_button)
    field_button.click()
    option = wait.until(EC.element_to_be_clickable((By.XPATH, '//span[@title="項目E"]')))
    option.click()

    # 商品リスト（複数選択）
    def select_dual_listbox_Cognition(labels):
        for label in labels:
            option_xpath = f'//div[@role="option"]//span[@title="{label}"]'
            option_element = wait.until(EC.element_to_be_clickable((By.XPATH, option_xpath)))
            option_element.click()
            move_button = wait.until(EC.element_to_be_clickable((By.XPATH, '//records-record-layout-row[1]//records-record-layout-item[2]//lightning-dual-listbox//lightning-button-icon[1]/button')))
            move_button.click()
            print(f"✅ 商品リストに {label} を追加")
            time.sleep(3)

    def select_dual_listbox_items(labels):
        for label in labels:
            option_xpath = f'//div[@role="option"]//span[@title="{label}"]'
            option_element = wait.until(EC.element_to_be_clickable((By.XPATH, option_xpath)))
            option_element.click()
            move_button = wait.until(EC.element_to_be_clickable((By.XPATH, '//records-record-layout-row[3]//records-record-layout-item[1]//lightning-dual-listbox//lightning-button-icon[1]/button')))
            move_button.click()
            print(f"✅ 商品リストに {label} を追加")
            time.sleep(3)
    select_dual_listbox_Cognition(["項目F"])
    driver.execute_script("window.scrollBy(0, 300);")
    select_dual_listbox_items(["項目G"])

    # 選択リスト：「項目H」
    lead_status_button = wait.until(EC.element_to_be_clickable((By.XPATH, '//label[text()="項目H"]/following::button[1]')))
    driver.execute_script("arguments[0].scrollIntoView(true);", lead_status_button)
    lead_status_button.click()

    # 参照関係：「項目I」
    lookup = wait.until(EC.presence_of_element_located((By.XPATH, '//input[@placeholder="項目Iを検索..."]')))
    lookup.send_keys("項目J")
    time.sleep(2)
    driver.execute_script("arguments[0].click();", wait.until(EC.element_to_be_clickable((By.XPATH, '//lightning-base-combobox-formatted-text'))))

    # 保存
    save_button = wait.until(EC.element_to_be_clickable((By.XPATH, '//button[@name="SaveEdit"]')))
    driver.execute_script("arguments[0].click();", save_button)
    time.sleep(3)
    detail_button = wait.until(EC.element_to_be_clickable((By.XPATH, '//button[@title="詳細"]')))
    wait.until(EC.presence_of_element_located((By.XPATH, '//a[contains(@href, "/Lead/")]')))
    driver.execute_script("arguments[0].scrollIntoView(true);", "//div[contains(@class, 'some-parent-class')]//span[contains(@class, 'test-id__field-label') and normalize-space(text())='項目K']")
    driver.save_screenshot("lead_after_save.png")
    print("✅ UIテスト完了（スクリーンショット保存）")

try:
    load_cookies_and_open_leads()
    create_lead_and_capture_screenshots()
finally:
    driver.quit()
