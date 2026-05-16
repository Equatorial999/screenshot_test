from playwright.sync_api import sync_playwright
import time

def run():
    with sync_playwright() as p:
        # 変更点1：解像度をフルHD（1920x1080）に設定して高画質化
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(viewport={'width': 1920, 'height': 1080})
        page = context.new_page()
        
        page.set_extra_http_headers({
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        })
        
        print("WSJのページにアクセスしています...")
        page.goto("https://www.wsj.com/market-data/stocks/peyields", timeout=60000)
        
        print("画面の描画を待っています...")
        time.sleep(10)
        
        # 変更点2：画面上のすべての「表（table）」の中身をテキストとして抽出して表示
        print("\n▼▼▼ 抽出した表データ ▼▼▼")
        tables = page.locator("table").all()
        if not tables:
            print("表が見つかりませんでした。")
        else:
            for i, table in enumerate(tables):
                print(f"--- 表 {i+1} ---")
                print(table.inner_text())
                print("----------------\n")
        
        page.screenshot(path="wsj_screenshot.png", full_page=True)
        print("スクリーンショットの撮影に成功しました！")
        
        browser.close()

if __name__ == "__main__":
    run()
