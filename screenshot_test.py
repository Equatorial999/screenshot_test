from playwright.sync_api import sync_playwright
import time

def run():
    with sync_playwright() as p:
        # 変更点：ブラウザの起動方法を少し変え、画面サイズ（解像度）を指定します
        # headless=True（画面を表示しないモード）は維持します
        browser = p.chromium.launch(headless=True)
        
        # フルHD（1920x1080）の仮想画面を作成します
        context = browser.new_context(viewport={'width': 1920, 'height': 1080})
        page = context.new_page()
        
        page.set_extra_http_headers({
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        })
        
        print("WSJのページにアクセスしています...")
        # 成功したタイムアウト設定（60秒）を維持します
        page.goto("https://www.wsj.com/market-data/stocks/peyields", timeout=60000)
        
        print("画面の描画を待っています...")
        # 成功した待機時間（10秒）を維持します
        time.sleep(10)
        
        # ページ全体のスクリーンショットを撮影
        page.screenshot(path="wsj_screenshot.png", full_page=True)
        print("高解像度でのスクリーンショット撮影に成功しました！")
        
        browser.close()

if __name__ == "__main__":
    run()
