from playwright.sync_api import sync_playwright
import time
from datetime import datetime
import base64
import requests

def run():
    with sync_playwright() as p:
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
        
        today_str = datetime.now().strftime("%Y-%m-%d")
        file_name = f"wsj_{today_str}.png"
        
        page.screenshot(path=file_name, full_page=True)
        print("スクリーンショットの撮影に成功しました。")
        browser.close()
        
        # ★★★ここにGASのウェブアプリURLを貼り付けてください★★★
        gas_url = "https://script.google.com/macros/s/AKfycbz2wxOTjdAaB2LUSqvn33dEjGF909ANLSb4gxL0EBxhHlJAR88d7bSHDOxAckozCsVC/exec"
        
        print("GAS（Googleドライブ）へ画像を送信しています...")
        with open(file_name, "rb") as image_file:
            encoded_string = base64.b64encode(image_file.read()).decode('utf-8')
            
            payload = {
                "image": encoded_string,
                "fileName": file_name
            }
            
            try:
                response = requests.post(gas_url, json=payload)
                response.raise_for_status()
                
                result = response.json()
                if result.get("status") == "success":
                    print(f"【大成功】Googleドライブへの保存とGmail送信が完了しました！ URL: {result.get('url')}")
                else:
                    print(f"【GAS側エラー】{result.get('message')}")
            except Exception as e:
                print(f"【通信エラー】発生しました: {e}")

if __name__ == "__main__":
    run()
