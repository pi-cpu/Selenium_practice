# Salesforce Lead UI 自動テスト（Selenium）

このリポジトリでは、**Selenium + Python** を用いて、Salesforce上の**Leadレコード作成をUI経由で自動化**するスクリプトを管理しています。

---

## ✅ 概要

- **目的**: SalesforceのLeadオブジェクトに対してUI経由で新規レコードを作成し、テストや動作確認を自動化する。
- **技術スタック**:
  - Python 3.11+
  - Selenium 4.x
  - Microsoft Edge（Chromium版）
- **対象UI**: Lightning Experience

---

## 📁 ファイル構成

Selenium_practice/
├── lead_ui_test_screenshot.py   # メインスクリプト（Lead作成＋スクリーンショット保存）
├── cookies.json                 # 手動で取得したSalesforceログインCookie
├── README.md                    # このファイル

---

## 🔧 準備手順

### 1. 必要なライブラリのインストール

```bash
pip install selenium

2. Microsoft Edgeドライバーのセットアップ
	•	Microsoft Edge バージョンに対応した msedgedriver.exe をインストールし、環境変数 PATH に追加するか、Pythonスクリプトと同じフォルダに配置してください。

3. SalesforceログインとCookieの取得
	•	EdgeでSalesforceにログイン（MFAなしアカウント推奨）
	•	開発者ツール（F12） > アプリケーション > Cookie > .salesforce.com ドメイン
	•	以下のCookieをコピーし、cookies.json に保存：

[
  {
    "name": "sid",
    "value": "xxxxxxxxxxxxx",
    "domain": ".salesforce.com",
    "path": "/",
    "secure": true,
    "httpOnly": true
  }
]


⸻

🚀 実行方法

python lead_ui_test_screenshot.py

	•	Salesforceに自動ログイン（Cookie使用）
	•	Lead一覧画面に遷移
	•	「新規作成」ボタンをクリック
	•	各種入力フィールドに自動入力
	•	スクリーンショットを保存（Before/After）

⸻

📝 自動入力されるフィールド

フィールド名	値（例）
姓	自動生成姓
会社名	自動生成会社
商品リスト（複数）	['IT', 'Jordan']
状況（選択リスト）	Working - Contacted
関連キャンペーン	DM Campaign to Top Customers


⸻

🖼️ スクリーンショット出力
	•	screenshots/before_update.png
	•	screenshots/after_update.png

⸻

⚠️ 注意事項
	•	Lightning UIは動的構造のため、XPathが変動することがあります。
	•	一部の要素はモーダルにより非表示状態になっていることがあり、click() の代わりに driver.execute_script(...) で対応しています。
	•	Salesforceの画面構成変更によりスクリプトが動かなくなる可能性があります。

⸻

📌 今後の展望（例）
	•	CIでのUIテスト実行対応（headlessモード）
	•	入力項目のJSON定義化
	•	他オブジェクト（商談、取引先）のUIテスト拡張

⸻

🧑‍💻 作成者
	•	Author: haha
	•	Salesforce開発者 / Python学習者

---

このテンプレは「自動UIテストスクリプトの成果物としての再利用」や「他人に見せる場合の説明文」にも使えます。  
変更・追記したい点があれば、お知らせください。必要に応じて「英語版」や「ヘッドレス環境対応版」も提供できます。
