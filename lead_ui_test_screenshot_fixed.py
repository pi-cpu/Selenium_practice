import json
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Edgeの設定
options = Options()
options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")
driver = webdriver.Edge(options=options)
wait = WebDriverWait(driver, 20)

# Cookieを読み込む
with open("cookies.json", "r", encoding="utf-8") as f:
    cookies = json.load(f)

driver.get("https://orgfarm-89e4339fa3-dev-ed.develop.my.salesforce.com/")
for cookie in cookies:
    driver.add_cookie(cookie)
driver.get("https://orgfarm-89e4339fa3-dev-ed.develop.my.salesforce.com/lightning/o/Lead/list?filterName=Recent")
print("✅ リード一覧画面の読み込み完了")

def create_lead_and_capture_screenshots():
    print("▶ Lead 新規作成を開始")
    driver.find_element(By.XPATH, '//a[@title="新規"]').click()
    time.sleep(3)
    driver.save_screenshot("lead_before_save.png")

    # テキスト
    wait.until(EC.presence_of_element_located((By.XPATH, '//label[text()="姓"]/following::input[1]'))).send_keys("自動生成姓")
    driver.find_element(By.XPATH, '//label[text()="会社名"]/following::input[1]').send_keys("自動生成会社")

    # 選択リスト：最終変更種別
    driver.find_element(By.XPATH, '//label[text()="最終変更種別"]/following::button[1]').click()
    time.sleep(1)
    driver.execute_script("arguments[0].click();", wait.until(EC.element_to_be_clickable((By.XPATH, '//span[@title="本人からの依頼"]'))))

    # 商品リスト（複数選択）
    def select_dual_listbox_items(labels):
        for label in labels:
            option_xpath = f'//span[@title="{label}"]/ancestor::div[@role="option"]'
            option_element = wait.until(EC.element_to_be_clickable((By.XPATH, option_xpath)))
            driver.execute_script("arguments[0].click();", option_element)
            time.sleep(0.5)

        move_button = wait.until(EC.element_to_be_clickable((By.XPATH, '//button[@title="選択済み に移動"]')))
        driver.execute_script("arguments[0].click();", move_button)
        print(f"✅ 商品リストに {labels} を追加")

    select_dual_listbox_items(["IT", "Jordan"])

    # 選択リスト：「リード 状況」
    driver.find_element(By.XPATH, '//label[text()="リード 状況"]/following::button[1]').click()
    time.sleep(1)
    driver.execute_script("arguments[0].click();", wait.until(EC.element_to_be_clickable((By.XPATH, '//span[@title="Working - Contacted"]'))))

    # 参照関係：「関連キャンペーン」
    lookup = wait.until(EC.presence_of_element_located((By.XPATH, '//input[@title="キャンペーンを検索"]')))
    lookup.send_keys("DM Campaign to Top Customers - Nov 12-23, 2001")
    time.sleep(2)
    driver.execute_script("arguments[0].click();", wait.until(EC.element_to_be_clickable((By.XPATH, '//lightning-base-combobox-formatted-text'))))

    # 保存
    wait.until(EC.element_to_be_clickable((By.XPATH, '//button[@name="SaveEdit"]'))).click()
    time.sleep(5)
    driver.save_screenshot("lead_after_save.png")
    print("✅ UIテスト完了（スクリーンショット保存）")

create_lead_and_capture_screenshots()
