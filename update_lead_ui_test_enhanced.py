# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver.common.by import By
import pickle
import time
import os

# Edge WebDriver起動
options = webdriver.EdgeOptions()
driver = webdriver.Edge(options=options)

# SalesforceインスタンスURL
BASE_URL = "https://orgfarm-89e4339fa3-dev-ed.develop.my.salesforce.com/"
LEAD_LIST_URL = f"{BASE_URL}/lightning/o/Lead/list?filterName=Recent"
COOKIE_FILE = "sf_cookies.pkl"

def load_cookies_and_open_lead_list():
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

    driver.get(LEAD_LIST_URL)
    time.sleep(5)

def update_multiple_leads_and_capture(n=3):
    for i in range(1, n + 1):
        print(f"▶ {i}件目のLeadレコードを編集中...")

        # レコードクリック（リスト内のi番目）
        row_xpath = f'(//table//tbody//tr)[{i}]'
        driver.find_element(By.XPATH, row_xpath).click()
        time.sleep(5)

        # 編集ボタン
        driver.find_element(By.XPATH, '//button[@name="Edit"]').click()
        time.sleep(3)

        # スクリーンショット（変更前）
        driver.save_screenshot(f"lead_{i}_before_update.png")

        # 「姓」
        last_name = driver.find_element(By.XPATH, '//label[text()="姓"]/following::input[1]')
        last_name.clear()
        last_name.send_keys(f"更新姓{i}")

        # 「会社名」
        company = driver.find_element(By.XPATH, '//label[text()="会社"]/following::input[1]')
        company.clear()
        company.send_keys(f"更新会社{i}")

        # 「最終変更種別」（選択リスト）
        driver.find_element(By.XPATH, '//label[text()="最終変更種別"]/following::div//button').click()
        time.sleep(1)
        driver.find_element(By.XPATH, '//span[@title="更新"]').click()

        # 「商品リスト」（複数選択リスト）
        driver.find_element(By.XPATH, '//label[text()="商品リスト"]/following::div//button').click()
        time.sleep(1)
        driver.find_element(By.XPATH, '//span[@title="製品A"]').click()
        driver.find_element(By.XPATH, '//span[@title="製品B"]').click()

        # 「リード 状況」（選択リスト）
        driver.find_element(By.XPATH, '//label[text()="リード 状況"]/following::div//button').click()
        time.sleep(1)
        driver.find_element(By.XPATH, '//span[@title="作業中"]').click()

        # 「関連キャンペーン」（参照関係）
        lookup_input = driver.find_element(By.XPATH, '//input[@title="キャンペーンを検索"]')
        lookup_input.clear()
        lookup_input.send_keys("サマーキャンペーン")
        time.sleep(3)
        driver.find_element(By.XPATH, '//lightning-base-combobox-formatted-text').click()

        # 保存
        driver.find_element(By.XPATH, '//button[@name="SaveEdit"]').click()
        time.sleep(6)

        # スクリーンショット（変更後）
        driver.save_screenshot(f"lead_{i}_after_update.png")
        print(f"✅ {i}件目 完了：lead_{i}_before_update.png / lead_{i}_after_update.png")

        # 一覧に戻る
        driver.get(LEAD_LIST_URL)
        time.sleep(5)

try:
    load_cookies_and_open_lead_list()
    update_multiple_leads_and_capture(n=3)
    print("✅ UI複数件更新テスト完了")
finally:
    driver.quit()
