from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

import time

def scroll_and_set_value(driver, wait, label_text, value):
    """
    ラベル名に基づいて input 要素を見つけ、スクロールして値を入力する。
    """
    try:
        # ラベルテキストの直後の input 要素を見つける
        xpath = f'//label[text()="{label_text}"]/following::input[1]'
        input_elem = wait.until(EC.presence_of_element_located((By.XPATH, xpath)))

        # スクロールして中央に表示
        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", input_elem)
        time.sleep(0.5)  # 描画安定のため

        # 入力操作
        input_elem.clear()
        input_elem.send_keys(value)
        print(f"✅ 入力完了: {label_text} → {value}")
        return True
    except Exception as e:
        print(f"❌ 入力失敗: {label_text} ({e})")
        return False