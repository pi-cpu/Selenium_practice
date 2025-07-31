# Salesforce ApexTriggerHandler UIテスト自動化（Edge + Selenium）

このリポジトリは、Salesforce の `Lead` オブジェクトに設定された Apex TriggerHandler の動作を、Microsoft Edge 上で UI 経由でテストし、スクリーンショットを取得する自動化スクリプトです。

---

## 📦 構成ファイル

| ファイル名 | 内容 |
|------------|------|
| `save_cookie.py` | Salesforce に手動ログイン後、Cookie を保存します |
| `lead_ui_test_screenshot.py` | Cookie を再利用してログイン済セッションで UI テストを実行し、スクリーンショットを取得します |
| `sf_cookies.pkl` | Cookie を保存するためのファイル（`save_cookie.py` 実行後に生成） |
| `requirements.txt` | Python の依存ライブラリ（`selenium`） |

---

## 🛠 使用方法

### 1. 必要ライブラリのインストール

```bash
pip install -r requirements.txt
```

---

### 2. Salesforce に手動ログインして Cookie を保存

```bash
python save_cookie.py
```

- 実行後、ブラウザが開きます
- 手動で Salesforce にログイン（MFA 含む）
- ログイン後にコンソールで Enter を押すと、`sf_cookies.pkl` が保存されます

---

### 3. UI テストスクリプトの実行

```bash
python lead_ui_test_screenshot.py
```

- `Lead` の新規レコードを UI 上で作成
- **保存前**と**保存後**のスクリーンショットをそれぞれ取得：
  - `lead_before_save.png`
  - `lead_after_save.png`

---

## ✅ テスト対象のフィールド

| 項目名 | 種別 | 入力値 | XPath例 |
|--------|------|--------|---------|
| 姓 | テキスト | テスト姓 | `//label[text()="姓"]/following::input[1]` |
| 会社 | テキスト | テスト会社 | `//label[text()="会社"]/following::input[1]` |
| 保存 | ボタン | - | `//button[@name="SaveEdit"]` |

---

## ✅ 注意事項

- Cookie は時間経過（1〜2時間）で無効になります。都度 `save_cookie.py` を再実行してください。
- Lightning UI の構造変化により、XPath は将来的に変更が必要になる場合があります。
- WebDriver（`msedgedriver`）は Edge バージョンと一致したものをインストールしてください。

---

## 📚 参考資料

- [Selenium公式ドキュメント](https://www.selenium.dev/documentation/)
- [Edge WebDriver](https://developer.microsoft.com/en-us/microsoft-edge/tools/webdriver/)
- [Salesforce Developer Guide](https://developer.salesforce.com/docs/)

---

## 🔒 免責

本ツールは業務自動化・検証支援を目的としており、本番環境への影響がないように注意してご使用ください。