from playwright.sync_api import sync_playwright
import time

def run():
    with sync_playwright() as p:
        # クラウド上の本物のブラウザ（Chromium）を起動
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        
        # 念のため、Bot判定を回避するための偽装用ブラウザ情報を設定
        page.set_extra_http_headers({
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        })
        
        print("WSJのページにアクセスしています...")
        page.goto("https://www.wsj.com/market-data/stocks/peyields", wait_until="networkidle")
        
        # 動的な表が完全に描画されるまで、少し（5秒）待つ
        print("画面の描画を待っています...")
        time.sleep(5)
        
        # ページ全体のスクリーンショットを撮影して保存
        page.screenshot(path="wsj_screenshot.png", full_page=True)
        print("スクリーンショットの撮影に成功しました！")
        
        browser.close()

if __name__ == "__main__":
    run()