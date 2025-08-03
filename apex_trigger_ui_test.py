# -*- coding: utf-8 -*-
"""
UI テスト自動化スクリプト – Salesforce のカスタム Apex トリガを検証するための例。

このスクリプトは Selenium WebDriver を使用して Salesforce 環境にログインし、
対象のオブジェクトのレコードを UI から新規作成して Apex トリガの処理結果を画面で確認します。

手順の概要:
1. cookie ファイルからセッション情報を読み込み、Salesforce にログインします。
2. 対象オブジェクトのリストビューを開き、新規レコード作成画面を表示します。
3. 必須項目やトリガを動作させる条件を入力します。
4. レコードを保存して、トリガによって設定された項目値や関連レコードを画面上で確認します。
5. 重要な画面のスクリーンショットを取得し、テスト結果を標準出力に出力します。
# -*- coding: utf-8 -*-
"""
UI テスト自動化スクリプト – Salesforce のカスタム Apex トリガを検証するための例。

このスクリプトは Selenium WebDriver を使用して Salesforce 環境にログインし、
対象のオブジェクトのレコードを UI から新規作成して Apex トリガの処理結果を画面で確認します。

手順の概要:
1. cookie ファイルからセッション情報を読み込み、Salesforce にログインします。
2. 対象オブジェクトのリストビューを開き、新規レコード作成画面を表示します。
3. 必須項目やトリガを動作させる条件を入力します。
4. レコードを保存して、トリガによって設定された項目値や関連レコードを画面上で確認します。
5. 重要な画面のスクリーンショットを取得し、テスト結果を標準出力に出力します。

※本コードは参考用のテンプレートです。実際のオブジェクト名や項目ラベル、検証項目は
  環境に合わせて編集してください。

参考:
マインドマジックスのブログによると、Salesforce は世界中の大手企業で利用されている代表的な CRM であり、
品質保証を実現するために自動化テストが重要であることが示されています【815863779379102†L141-L148】。
単体テストだけでは Apex のカスタムコードのみを対象とするため、統合的な検証には UI テストも必要であると
述べられています【815863779379102†L155-L163】。Selenium はウェブアプリケーション向けの信頼性の高い
テストフレームワークであり、Python などの言語で記述したテストを Chrome や Edge などのブラウザ上で
実行できることが紹介されています【815863779379102†L165-L176】。このスクリプトでは Selenium を利用して
Salesforce の UI を操作し、ユーザ操作の再現やテストデータの入力、画面上での結果確認を自動化します。
"""

import json
import time
from pathlib import Path

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
f
rom selenium.webdriver.edge.service import Service
from selenium.webdriver.edge.options import Options

# -----------------------------------------------------------------------------
# 設定値 – 環境に応じて変更してください
# -----------------------------------------------------------------------------
# Cookie を保存したファイル名。Salesforce ログイン済みブラウザからエクスポートした
# JSON 形式の Cookie を用意する必要があります。
COOKIE_FILE = "manual_cookies.json"

# ログイン先組織のベース URL。例: "https://xxx.my.salesforce.com/"
BASE_URL = "https://cybernet--takahara.sandbox.my.salesforce.com/"

# テスト対象オブジェクトの API 名。カスタムオブジェクトの場合は末尾に "__c" を付けます。
OBJECT_API_NAME = "CustomObject__c"

# トリガによって設定される項目（ラベル）と期待値。
# ここで指定したラベルの項目を詳細画面から取得し、値が期待通りか検証します。
TRIGGER_FIELD_LABEL = "結果項目ラベル"
EXPECTED_TRIGGER_VALUE = "トリガ更新後の期待値"

# 計測に使用する WebDriver の実行ファイルパス。ローカル環境のドライバに合わせて変更すること。
EDGE_DRIVER_PATH = r"C:/WebDriver/MicrosoftEdgeDeveloper/msedgedriver.exe"

# -----------------------------------------------------------------------------
# Selenium セットアップ
# -----------------------------------------------------------------------------

def init_driver() -> webdriver.Edge:
    """Edge WebDriver を初期化して返します。"""
    options = Options()
    # 通知ダイアログを無効化
    options.add_argument("--disable-notifications")
    # 画面サイズを固定（必要に応じて変更）
    options.add_argument("--window-size=1280,1024")
    service = Service(executable_path=EDGE_DRIVER_PATH)
    driver = webdriver.Edge(service=service, options=options)
    return driver


def load_cookies(driver: webdriver.Edge, cookie_path: str) -> None:
    """JSON ファイルから Cookie を読み込み、WebDriver に設定してログインセッションを復元します。"""
    cookie_file = Path(cookie_path)
    if not cookie_file.is_file():
        raise FileNotFoundError(f"Cookie ファイル {cookie_path} が見つかりません。ログイン済みのブラウザから cookie をエクスポートしてください。")
    driver.get(BASE_URL)
    # ページを 3 秒ほど待ち、Salesforce のドメインに Cookie を設定可能にする
    time.sleep(3)
    with cookie_file.open("r", encoding="utf-8") as f:
        cookies = json.load(f)
    # JSON に expiry が含まれると add_cookie でエラーになるため削除
    for cookie in cookies:
        cookie.pop("expiry", None)
        # domain の設定がない場合は *.my.salesforce.com として扱う
        cookie.setdefault("domain", ".my.salesforce.com")
        cookie["secure"] = True
        cookie.setdefault("sameSite", "None")
        try:
            driver.add_cookie(cookie)
        except Exception as e:
            print(f"Warning: cookie {cookie.get('name')} の追加に失敗しました: {e}")


def open_object_list_view(driver: webdriver.Edge) -> None:
    """対象オブジェクトのリストビューを開き、画面読み込み完了を待ちます。"""
    list_url = f"{BASE_URL}/lightning/o/{OBJECT_API_NAME}/list?filterName=RecentlyViewed"
    driver.get(list_url)
    wait = WebDriverWait(driver, 30)
    # オブジェクトリストの「新規」ボタンが表示されるまで待つ
    wait.until(EC.presence_of_element_located((By.XPATH, '//a[@title="新規"]')))
    print("✅ オブジェクト一覧画面の読み込み完了")


def create_record_and_capture(driver: webdriver.Edge) -> None:
    """
    新規レコードを作成してトリガの動作を確認するメイン処理。

    1. 「新規」ボタンを押して入力画面を表示
    2. 必須項目やトリガ条件を入力
    3. 保存後に詳細画面からトリガ結果項目を取得し、期待値と比較
    4. 前後でスクリーンショットを取得
    """
    wait = WebDriverWait(driver, 30)

    print("▶ レコード新規作成を開始")
    # 新規ボタンをクリック
    new_button = wait.until(EC.element_to_be_clickable((By.XPATH, '//a[@title="新規"]')))
    new_button.click()
    time.sleep(2)
    driver.save_screenshot("before_create.png")

    # 以下は例示的な項目入力処理です。実際の項目ラベルや入力内容に合わせて編集してください。
    # テキスト項目の入力例
    try:
        name_field = wait.until(EC.element_to_be_clickable((By.XPATH, '//label[text()="項目A"]/following::input[1]')))
        name_field.send_keys("自動生成データA")
    except Exception:

      print("⚠️ 項目A の入力フィールドが見つかりませんでした。項目ラベルを確認してください。")

    # 選択リスト項目の選択例
    try:
        picklist_button = wait.until(EC.element_to_be_clickable((By.XPATH, '//label[text()="項目B"]/following::button[1]')))
        picklist_button.click()
        # 選択肢タイトルが「選択肢1」のものを選ぶ例
        option = wait.until(EC.element_to_be_clickable((By.XPATH, '//span[@title="選択肢1"]')))
        option.click()
    except Exception:
        print("⚠️ 項目B の選択リストが見つかりませんでした。ラベルや選択肢を確認してください。")

    # その他必要な入力を追加してください

  # 入力する項目設定
TEXT_FIELDS = {
    "項目A": "自動生成データA",
    # 必要に応じて追加
}

SELECT_FIELDS = {
    "項目B": "選択肢1",
    # 必要に応じて追加
}

MULTI_SELECT_FIELDS = {
    # 例: "項目C": ["値1", "値2"]
}

def create_record_and_capture(driver: webdriver.Edge) -> None:
    """新規レコードを作成してトリガの動作を確認するメイン処理。"""
    wait = WebDriverWait(driver, 30)
    print("▶ レコード新規作成を開始")
    new_button = wait.until(EC.element_to_be_clickable((By.XPATH, '//a[@title="新規"]')))
    new_button.click()
    time.sleep(2)
    driver.save_screenshot("before_create.png")

    # テキスト項目入力
    for label, value in TEXT_FIELDS.items():
        try:
            input_field = wait.until(EC.element_to_be_clickable((By.XPATH, f'//label[text()="{label}"]/following::input[1]')))
            input_field.clear()
            input_field.send_keys(value)
        except Exception:
            print(f"⚠️ テキスト項目 '{label}' の入力フィールドが見つかりません")

    # 単一選択リスト
    for label, option_value in SELECT_FIELDS.items():
        try:
            picklist_button = wait.until(EC.element_to_be_clickable((By.XPATH, f'//label[text()="{label}"]/following::button[1]')))
            picklist_button.click()
            option = wait.until(EC.element_to_be_clickable((By.XPATH, f'//span[@title="{option_value}"]')))
            option.click()
        except Exception:
            print(f"⚠️ 選択リスト項目 '{label}' または選択肢 '{option_value}' が見つかりません")

    # 複数選択リスト（マルチセレクトピックリスト）の設定
    # キーにフィールドラベル、値に選択したい項目のリストを指定します。
    MULTI_SELECT_FIELDS = {
        "趣味": ["登山", "映画鑑賞", "料理"],
        "対応サービス": ["保守サポート", "クラウド利用"],
        # 必要に応じて他のマルチセレクト項目を追加
    }

# マルチセレクト項目を処理する共通関数例（create / update 両方で利用可能）
def fill_multiselect_fields(driver: webdriver.Edge, wait: WebDriverWait) -> None:
    """
    ページ内の複数選択リストをまとめて入力します。
    MULTI_SELECT_FIELDS で指定したラベルのフィールドを検索し、各値を選択します。
    """
    for label, options in MULTI_SELECT_FIELDS.items():
        try:
            # ラベルテキストに続くマルチセレクトのコンテナを取得
            # 「following::*[contains(@class,"forceInputMultiPicklist")]」で対象セクションを絞り込み
            container = wait.until(EC.element_to_be_clickable((
                By.XPATH,
                f'//label[normalize-space()="{label}"]/following::*[contains(@class,"forceInputMultiPicklist")]'
            )))
            # コンテナ内のボタンをクリックしてピックリストを開く
            button = container.find_element(By.TAG_NAME, "button")
            button.click()

            # 指定された各選択肢をクリック
            for opt in options:
                option_elem = wait.until(EC.element_to_be_clickable((
                    By.XPATH, f'//span[@title="{opt}"]'
                )))
                option_elem.click()

            # 選択終了後、ダイアログの外側をクリックしてポップアップを閉じる
            driver.find_element(By.XPATH, '//div[contains(@class, "modal-container")]').click()
        except Exception as e:
            print(f"⚠️ マルチセレクト項目 '{label}' の処理でエラーが発生しました: {e}")

# create_record_and_capture() での使用例

# update_record_and_capture() でも同様に fill_multiselect_fields() を呼び出して更新処理を行います。


    # トリガ項目の検証（旧コードと同様）
    # ...

def update_record_and_capture(driver: webdriver.Edge) -> None:
    """既存レコードを更新し、トリガの再検証を行います。"""
    wait = WebDriverWait(driver, 30)
    print("▶ レコード更新を開始")
    try:
        first_row_link = wait.until(EC.element_to_be_clickable((By.XPATH, '//table//tbody/tr[1]//a[contains(@class,"outputLookupLink")]')))
        first_row_link.click()
    except Exception:
        print("⚠️ レコードリンクが取得できません")
        return

    wait.until(EC.presence_of_element_located((By.XPATH, '//button[@title="詳細"]')))
    try:
        edit_button = wait.until(EC.element_to_be_clickable((By.XPATH, '//button[@title="編集"]')))
        edit_button.click()
    except Exception:
        # リンク形式の場合も考慮
        edit_link = wait.until(EC.element_to_be_clickable((By.XPATH, '//a[@title="編集"]')))
        edit_link.click()

    time.sleep(2)
    driver.save_screenshot("before_update.png")

    # 更新処理：TEXT_FIELDS の値にサフィックス「_更新」を付与
    for label, value in TEXT_FIELDS.items():
        try:
            field = wait.until(EC.element_to_be_clickable((By.XPATH, f'//label[text()="{label}"]/following::input[1]')))
            field.clear()
            field.send_keys(value + "_更新")
        except Exception:
            print(f"⚠️ 更新: テキスト項目 '{label}' が見つかりません")

    # 単一選択リスト更新
    for label, option_value in SELECT_FIELDS.items():
        try:
            btn = wait.until(EC.element_to_be_clickable((By.XPATH, f'//label[text()="{label}"]/following::button[1]')))
            btn.click()
            option = wait.until(EC.element_to_be_clickable((By.XPATH, f'//span[@title="{option_value}"]')))
            option.click()
        except Exception:
            print(f"⚠️ 更新: 選択リスト項目 '{label}' が見つかりません")

    # 複数選択リスト更新
    for label, options in MULTI_SELECT_FIELDS.items():
        try:
            button = wait.until(EC.element_to_be_clickable((By.XPATH, f'//label[text()="{label}"]/following::*[contains(@class,"forceInputMultiPicklist")]//button')))
            button.click()
            for opt in options:
                option = wait.until(EC.element_to_be_clickable((By.XPATH, f'//span[@title="{opt}"]')))
                option.click()
            driver.find_element(By.XPATH, '//div[contains(@class, "modal-container")]').click()
        except Exception:
            print(f"⚠️ 更新: 複数選択項目 '{label}' の処理でエラーが発生しました")

    # 保存ボタン
    save_button = wait.until(EC.element_to_be_clickable((By.XPATH, '//button[@name="SaveEdit"]')))
    save_button.click()

    time.sleep(5)
    wait.until(EC.presence_of_element_located((By.XPATH, '//button[@title="詳細"]')))
    driver.save_screenshot("after_update.png")

    # 更新後のトリガ項目検証（作成時と同様に取得・比較）
    # ...

def main() -> None:
    """テストのエントリポイント。作成および更新テストを順に実行します。"""
    driver = init_driver()
    try:
        load_cookies(driver, COOKIE_FILE)
        open_object_list_view(driver)
        create_record_and_capture(driver)
        open_object_list_view(driver)     # 更新前にリストビューへ戻る
        update_record_and_capture(driver)
    finally:
        driver.quit()


    # 保存ボタンをクリック
    try:
        wait = WebDriverWait(driver, 30)
        save_button = wait.until(EC.element_to_be_clickable((By.XPATH, '//button[@name="SaveEdit"]')))
        save_button.click()
    except Exception:
        print("⚠️ 保存ボタンが見つかりません。XPATH を確認してください。")
        return

    # 保存処理完了まで待機
    time.sleep(5)
    # 詳細画面が表示されるまで待つ（URL が /<objectId>/view になる）
    wait.until(EC.presence_of_element_located((By.XPATH, '//button[@title="詳細"]')))
    driver.save_screenshot("after_create.png")

    # トリガが設定した結果項目の値を取得し、期待値と比較
    try:
        # 詳細画面のフィールドラベルを基に値要素を取得する例。
        # Lightning Experience ではフィールドのラベルと値が別要素となるため、
        # ラベルから祖先をたどって値要素を取得する方法を採用します。
        label_element = wait.until(
            EC.presence_of_element_located((By.XPATH, f'//span[contains(@class, "test-id__field-label") and normalize-space(text())="{TRIGGER_FIELD_LABEL}"]'))
        )
        # ラベル要素から最も近い値要素を取得（同じレコードレイアウト行内を想定）
        value_element = label_element.find_element(By.XPATH, '../../following-sibling::div//span[@data-output-element-id]')
        actual_value = value_element.text.strip()
        print(f"⭐ トリガ項目 '{TRIGGER_FIELD_LABEL}' の値: {actual_value}")
        if actual_value == EXPECTED_TRIGGER_VALUE:
            print("✅ トリガの検証に成功しました (期待値と一致)")
        else:
            print(f"❌ 期待値 '{EXPECTED_TRIGGER_VALUE}' と一致しません: {actual_value}")
    except Exception:
        print("⚠️ トリガの結果項目を取得できませんでした。ページ構造や XPATH を確認してください。")


def main() -> None:
    """エントリポイント: ドライバの初期化からテスト完了までの一連処理を実行します。"""
    driver = init_driver()
    try:
        load_cookies(driver, COOKIE_FILE)
        open_object_list_view(driver)
        create_record_and_capture(driver)
    finally:
        # ブラウザを閉じる
        driver.quit()


if __name__ == "__main__":
    main()

※本コードは参考用のテンプレートです。実際のオブジェクト名や項目ラベル、検証項目は
  環境に合わせて編集してください。

参考:
マインドマジックスのブログによると、Salesforce は世界中の大手企業で利用されている代表的な CRM であり、
品質保証を実現するために自動化テストが重要であることが示されています【815863779379102†L141-L148】。
単体テストだけでは Apex のカスタムコードのみを対象とするため、統合的な検証には UI テストも必要であると
述べられています【815863779379102†L155-L163】。Selenium はウェブアプリケーション向けの信頼性の高い
テストフレームワークであり、Python などの言語で記述したテストを Chrome や Edge などのブラウザ上で
実行できることが紹介されています【815863779379102†L165-L176】。このスクリプトでは Selenium を利用して
Salesforce の UI を操作し、ユーザ操作の再現やテストデータの入力、画面上での結果確認を自動化します。
"""

import json
import time
from pathlib import Path

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.edge.service import Service
from selenium.webdriver.edge.options import Options

# -----------------------------------------------------------------------------
# 設定値 – 環境に応じて変更してください
# -----------------------------------------------------------------------------
# Cookie を保存したファイル名。Salesforce ログイン済みブラウザからエクスポートした
# JSON 形式の Cookie を用意する必要があります。
COOKIE_FILE = "manual_cookies.json"

# ログイン先組織のベース URL。例: "https://xxx.my.salesforce.com/"
BASE_URL = "https://cybernet--takahara.sandbox.my.salesforce.com/"

# テスト対象オブジェクトの API 名。カスタムオブジェクトの場合は末尾に "__c" を付けます。
OBJECT_API_NAME = "CustomObject__c"

# トリガによって設定される項目（ラベル）と期待値。
# ここで指定したラベルの項目を詳細画面から取得し、値が期待通りか検証します。
TRIGGER_FIELD_LABEL = "結果項目ラベル"
EXPECTED_TRIGGER_VALUE = "トリガ更新後の期待値"

# 計測に使用する WebDriver の実行ファイルパス。ローカル環境のドライバに合わせて変更すること。
EDGE_DRIVER_PATH = r"C:/WebDriver/MicrosoftEdgeDeveloper/msedgedriver.exe"

# -----------------------------------------------------------------------------
# Selenium セットアップ
# -----------------------------------------------------------------------------

def init_driver() -> webdriver.Edge:
    """Edge WebDriver を初期化して返します。"""
    options = Options()
    # 通知ダイアログを無効化
    options.add_argument("--disable-notifications")
    # 画面サイズを固定（必要に応じて変更）
    options.add_argument("--window-size=1280,1024")
    service = Service(executable_path=EDGE_DRIVER_PATH)
    driver = webdriver.Edge(service=service, options=options)
    return driver


def load_cookies(driver: webdriver.Edge, cookie_path: str) -> None:
    """JSON ファイルから Cookie を読み込み、WebDriver に設定してログインセッションを復元します。"""
    cookie_file = Path(cookie_path)
    if not cookie_file.is_file():
        raise FileNotFoundError(f"Cookie ファイル {cookie_path} が見つかりません。ログイン済みのブラウザから cookie をエクスポートしてください。")
    driver.get(BASE_URL)
    # ページを 3 秒ほど待ち、Salesforce のドメインに Cookie を設定可能にする
    time.sleep(3)
    with cookie_file.open("r", encoding="utf-8") as f:
        cookies = json.load(f)
    # JSON に expiry が含まれると add_cookie でエラーになるため削除
    for cookie in cookies:
        cookie.pop("expiry", None)
        # domain の設定がない場合は *.my.salesforce.com として扱う
        cookie.setdefault("domain", ".my.salesforce.com")
        cookie["secure"] = True
        cookie.setdefault("sameSite", "None")
        try:
            driver.add_cookie(cookie)
        except Exception as e:
            print(f"Warning: cookie {cookie.get('name')} の追加に失敗しました: {e}")


def open_object_list_view(driver: webdriver.Edge) -> None:
    """対象オブジェクトのリストビューを開き、画面読み込み完了を待ちます。"""
    list_url = f"{BASE_URL}/lightning/o/{OBJECT_API_NAME}/list?filterName=RecentlyViewed"
    driver.get(list_url)
    wait = WebDriverWait(driver, 30)
    # オブジェクトリストの「新規」ボタンが表示されるまで待つ
    wait.until(EC.presence_of_element_located((By.XPATH, '//a[@title="新規"]')))
    print("✅ オブジェクト一覧画面の読み込み完了")


def create_record_and_capture(driver: webdriver.Edge) -> None:
    """
    新規レコードを作成してトリガの動作を確認するメイン処理。

    1. 「新規」ボタンを押して入力画面を表示
    2. 必須項目やトリガ条件を入力
    3. 保存後に詳細画面からトリガ結果項目を取得し、期待値と比較
    4. 前後でスクリーンショットを取得
    """
    wait = WebDriverWait(driver, 30)

    print("▶ レコード新規作成を開始")
    # 新規ボタンをクリック
    new_button = wait.until(EC.element_to_be_clickable((By.XPATH, '//a[@title="新規"]')))
    new_button.click()
    time.sleep(2)
    driver.save_screenshot("before_create.png")

    # 以下は例示的な項目入力処理です。実際の項目ラベルや入力内容に合わせて編集してください。
    # テキスト項目の入力例
    try:
        name_field = wait.until(EC.element_to_be_clickable((By.XPATH, '//label[text()="項目A"]/following::input[1]')))
        name_field.send_keys("自動生成データA")
    except Exception:
        print("⚠️ 項目A の入力フィールドが見つかりませんでした。項目ラベルを確認してください。")

    # 選択リスト項目の選択例
    try:
        picklist_button = wait.until(EC.element_to_be_clickable((By.XPATH, '//label[text()="項目B"]/following::button[1]')))
        picklist_button.click()
        # 選択肢タイトルが「選択肢1」のものを選ぶ例
        option = wait.until(EC.element_to_be_clickable((By.XPATH, '//span[@title="選択肢1"]')))
        option.click()
    except Exception:
        print("⚠️ 項目B の選択リストが見つかりませんでした。ラベルや選択肢を確認してください。")

    # その他必要な入力を追加してください

  # 入力する項目設定
TEXT_FIELDS = {
    "項目A": "自動生成データA",
    # 必要に応じて追加
}

SELECT_FIELDS = {
    "項目B": "選択肢1",
    # 必要に応じて追加
}

MULTI_SELECT_FIELDS = {
    # 例: "項目C": ["値1", "値2"]
}

def create_record_and_capture(driver: webdriver.Edge) -> None:
    """新規レコードを作成してトリガの動作を確認するメイン処理。"""
    wait = WebDriverWait(driver, 30)
    print("▶ レコード新規作成を開始")
    new_button = wait.until(EC.element_to_be_clickable((By.XPATH, '//a[@title="新規"]')))
    new_button.click()
    time.sleep(2)
    driver.save_screenshot("before_create.png")

    # テキスト項目入力
    for label, value in TEXT_FIELDS.items():
        try:
            input_field = wait.until(EC.element_to_be_clickable((By.XPATH, f'//label[text()="{label}"]/following::input[1]')))
            input_field.clear()
            input_field.send_keys(value)
        except Exception:
            print(f"⚠️ テキスト項目 '{label}' の入力フィールドが見つかりません")

    # 単一選択リスト
    for label, option_value in SELECT_FIELDS.items():
        try:
            picklist_button = wait.until(EC.element_to_be_clickable((By.XPATH, f'//label[text()="{label}"]/following::button[1]')))
            picklist_button.click()
            option = wait.until(EC.element_to_be_clickable((By.XPATH, f'//span[@title="{option_value}"]')))
            option.click()
        except Exception:
            print(f"⚠️ 選択リスト項目 '{label}' または選択肢 '{option_value}' が見つかりません")

    # 複数選択リスト（マルチセレクトピックリスト）の設定
# キーにフィールドラベル、値に選択したい項目のリストを指定します。
MULTI_SELECT_FIELDS = {
    "趣味": ["登山", "映画鑑賞", "料理"],
    "対応サービス": ["保守サポート", "クラウド利用"],
    # 必要に応じて他のマルチセレクト項目を追加
}

# マルチセレクト項目を処理する共通関数例（create / update 両方で利用可能）
def fill_multiselect_fields(driver: webdriver.Edge, wait: WebDriverWait) -> None:
    """
    ページ内の複数選択リストをまとめて入力します。
    MULTI_SELECT_FIELDS で指定したラベルのフィールドを検索し、各値を選択します。
    """
    for label, options in MULTI_SELECT_FIELDS.items():
        try:
            # ラベルテキストに続くマルチセレクトのコンテナを取得
            # 「following::*[contains(@class,"forceInputMultiPicklist")]」で対象セクションを絞り込み
            container = wait.until(EC.element_to_be_clickable((
                By.XPATH,
                f'//label[normalize-space()="{label}"]/following::*[contains(@class,"forceInputMultiPicklist")]'
            )))
            # コンテナ内のボタンをクリックしてピックリストを開く
            button = container.find_element(By.TAG_NAME, "button")
            button.click()

            # 指定された各選択肢をクリック
            for opt in options:
                option_elem = wait.until(EC.element_to_be_clickable((
                    By.XPATH, f'//span[@title="{opt}"]'
                )))
                option_elem.click()

            # 選択終了後、ダイアログの外側をクリックしてポップアップを閉じる
            driver.find_element(By.XPATH, '//div[contains(@class, "modal-container")]').click()
        except Exception as e:
            print(f"⚠️ マルチセレクト項目 '{label}' の処理でエラーが発生しました: {e}")

# create_record_and_capture() での使用例
def create_record_and_capture(driver: webdriver.Edge) -> None:
    # …テキスト項目や単一選択リストの処理…
    # 複数選択リストを入力
    fill_multiselect_fields(driver, wait)
    # …保存とトリガ検証…

# update_record_and_capture() でも同様に fill_multiselect_fields() を呼び出して更新処理を行います。


    # トリガ項目の検証（旧コードと同様）
    # ...

def update_record_and_capture(driver: webdriver.Edge) -> None:
    """既存レコードを更新し、トリガの再検証を行います。"""
    wait = WebDriverWait(driver, 30)
    print("▶ レコード更新を開始")
    try:
        first_row_link = wait.until(EC.element_to_be_clickable((By.XPATH, '//table//tbody/tr[1]//a[contains(@class,"outputLookupLink")]')))
        first_row_link.click()
    except Exception:
        print("⚠️ レコードリンクが取得できません")
        return

    wait.until(EC.presence_of_element_located((By.XPATH, '//button[@title="詳細"]')))
    try:
        edit_button = wait.until(EC.element_to_be_clickable((By.XPATH, '//button[@title="編集"]')))
        edit_button.click()
    except Exception:
        # リンク形式の場合も考慮
        edit_link = wait.until(EC.element_to_be_clickable((By.XPATH, '//a[@title="編集"]')))
        edit_link.click()

    time.sleep(2)
    driver.save_screenshot("before_update.png")

    # 更新処理：TEXT_FIELDS の値にサフィックス「_更新」を付与
    for label, value in TEXT_FIELDS.items():
        try:
            field = wait.until(EC.element_to_be_clickable((By.XPATH, f'//label[text()="{label}"]/following::input[1]')))
            field.clear()
            field.send_keys(value + "_更新")
        except Exception:
            print(f"⚠️ 更新: テキスト項目 '{label}' が見つかりません")

    # 単一選択リスト更新
    for label, option_value in SELECT_FIELDS.items():
        try:
            btn = wait.until(EC.element_to_be_clickable((By.XPATH, f'//label[text()="{label}"]/following::button[1]')))
            btn.click()
            option = wait.until(EC.element_to_be_clickable((By.XPATH, f'//span[@title="{option_value}"]')))
            option.click()
        except Exception:
            print(f"⚠️ 更新: 選択リスト項目 '{label}' が見つかりません")

    # 複数選択リスト更新
    for label, options in MULTI_SELECT_FIELDS.items():
        try:
            button = wait.until(EC.element_to_be_clickable((By.XPATH, f'//label[text()="{label}"]/following::*[contains(@class,"forceInputMultiPicklist")]//button')))
            button.click()
            for opt in options:
                option = wait.until(EC.element_to_be_clickable((By.XPATH, f'//span[@title="{opt}"]')))
                option.click()
            driver.find_element(By.XPATH, '//div[contains(@class, "modal-container")]').click()
        except Exception:
            print(f"⚠️ 更新: 複数選択項目 '{label}' の処理でエラーが発生しました")

    # 保存ボタン
    save_button = wait.until(EC.element_to_be_clickable((By.XPATH, '//button[@name="SaveEdit"]')))
    save_button.click()

    time.sleep(5)
    wait.until(EC.presence_of_element_located((By.XPATH, '//button[@title="詳細"]')))
    driver.save_screenshot("after_update.png")

    # 更新後のトリガ項目検証（作成時と同様に取得・比較）
    # ...

def main() -> None:
    """テストのエントリポイント。作成および更新テストを順に実行します。"""
    driver = init_driver()
    try:
        load_cookies(driver, COOKIE_FILE)
        open_object_list_view(driver)
        create_record_and_capture(driver)
        open_object_list_view(driver)     # 更新前にリストビューへ戻る
        update_record_and_capture(driver)
    finally:
        driver.quit()


    # 保存ボタンをクリック
    try:
        save_button = wait.until(EC.element_to_be_clickable((By.XPATH, '//button[@name="SaveEdit"]')))
        save_button.click()
    except Exception:
        print("⚠️ 保存ボタンが見つかりません。XPATH を確認してください。")
        return

    # 保存処理完了まで待機
    time.sleep(5)
    # 詳細画面が表示されるまで待つ（URL が /<objectId>/view になる）
    wait.until(EC.presence_of_element_located((By.XPATH, '//button[@title="詳細"]')))
    driver.save_screenshot("after_create.png")

    # トリガが設定した結果項目の値を取得し、期待値と比較
    try:
        # 詳細画面のフィールドラベルを基に値要素を取得する例。
        # Lightning Experience ではフィールドのラベルと値が別要素となるため、
        # ラベルから祖先をたどって値要素を取得する方法を採用します。
        label_element = wait.until(
       
          EC.presence_of_element_located((By.XPATH, f'//span[contains(@class, "test-id__field-label") and normalize-space(text())="{TRIGGER_FIELD_LABEL}"]'))
        )
        # ラベル要素から最も近い値要素を取得（同じレコードレイアウト行内を想定）
        value_element = label_element.find_element(By.XPATH, '../../following-sibling::div//span[@data-output-element-id]')
        actual_value = value_element.text.strip()
        print(f"⭐ トリガ項目 '{TRIGGER_FIELD_LABEL}' の値: {actual_value}")
        if actual_value == EXPECTED_TRIGGER_VALUE:
            print("✅ トリガの検証に成功しました (期待値と一致)")
        else:
            print(f"❌ 期待値 '{EXPECTED_TRIGGER_VALUE}' と一致しません: {actual_value}")
    except Exception:
        print("⚠️ トリガの結果項目を取得できませんでした。ページ構造や XPATH を確認してください。")


def main() -> None:
    """エントリポイント: ドライバの初期化からテスト完了までの一連処理を実行します。"""
    driver = init_driver()
    try:
        load_cookies(driver, COOKIE_FILE)
        open_object_list_view(driver)
        create_record_and_capture(driver)
    finally:
        # ブラウザを閉じる
        driver.quit()


if __name__ == "__main__":
    main()
