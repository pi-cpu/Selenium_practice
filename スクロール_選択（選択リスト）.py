def select_single_picklist(driver, wait, label_text, option_text):
    try:
        # ピックリストのtextboxを取得
        input_xpath = f'//label[text()="{label_text}"]/following::input[1]'
        picklist_input = wait.until(EC.presence_of_element_located((By.XPATH, input_xpath)))
        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", picklist_input)
        time.sleep(0.3)
        picklist_input.click()

        # 選択肢を選ぶ
        option_xpath = f'//lightning-base-combobox-item//span[text()="{option_text}"]'
        option = wait.until(EC.element_to_be_clickable((By.XPATH, option_xpath)))
        option.click()

        print(f"✅ 選択完了: {label_text} → {option_text}")
        return True
    except Exception as e:
        print(f"❌ 選択失敗: {label_text} → {option_text} ({e})")
        return False