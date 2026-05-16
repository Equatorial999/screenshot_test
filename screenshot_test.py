from playwright.sync_api import sync_playwright
import time

def run():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        
        page.set_extra_http_headers({
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        })
        
        print("WSJのページにアクセスしています...")
        # 変更点1：networkidleを削除し、タイムアウトの限界を60秒（60000ms）に延長
        page.goto("https://www.wsj.com/market-data/stocks/peyields", timeout=60000)
        
        # 変更点2：重いページの描画を待つため、待機時間を10秒に延長
        print("画面の描画を待っています...")
        time.sleep(10)
        
        page.screenshot(path="wsj_screenshot.png", full_page=True)
        print("スクリーンショットの撮影に成功しました！")
        
        browser.close()

if __name__ == "__main__":
    run()
