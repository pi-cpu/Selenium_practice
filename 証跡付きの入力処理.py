# 1. 要素を取得してスクロール
target = wait.until(EC.presence_of_element_located((By.XPATH, '//input[@id="name-input"]')))
driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", target)
time.sleep(1)

# 2. 値を入力
target.clear()
target.send_keys("高原")

# 3. 入力後の画面を証跡として保存
driver.save_screenshot("after_input.png")