
from selenium import webdriver
import pickle
import time

# Edge WebDriver起動
options = webdriver.EdgeOptions()
driver = webdriver.Edge(options=options)

# Salesforceログインページへアクセス
driver.get("https://login.salesforce.com")
print("▶ 手動でログインしてください（MFA含む）")
input("ログイン後、Enterを押してください：")

# Cookie保存
with open("sf_cookies.pkl", "wb") as f:
    pickle.dump(driver.get_cookies(), f)

print("✅ Cookie 保存完了：sf_cookies.pkl")
driver.quit()
