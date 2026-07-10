# 最新版の修正内容：WSJページのタイムアウト対策として、domcontentloadedでの待機(90秒)、"Other Indexes"の出現待機(60秒)、および強制待機(30秒)を追加し、部分的な読み込みエラー(S&P500の欠落等)を防止。
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
        # 1. ページ自体の読み込みタイムアウトを「90秒」に延長し、HTML骨組みが出た段階(domcontentloaded)でOKとする
        try:
            page.goto("https://www.wsj.com/market-data/stocks/peyields", timeout=90000, wait_until="domcontentloaded")
            print("ページのHTML骨組みを読み込みました。")
        except Exception as e:
            print(f"goto時にタイムアウトが発生しましたが続行します: {e}")
        
        # 2. 肝心の「Other Indexes (S&P500などがある表)」の文字が画面に出現するまで、最大「60秒」待ち伏せする
        try:
            page.wait_for_selector("text=Other Indexes", timeout=60000)
            print("Other Indexesの表が出現したのを確認しました。")
        except Exception as e:
            print(f"表の出現確認でタイムアウトしましたが続行します: {e}")
        
        # 3. 数字が完全に表示されきるのを待つため、可能な限り長く「30秒（30000ms）」強制的に無条件待機する
        print("すべてのデータが描画されるよう、さらに30秒間待機します...")
        page.wait_for_timeout(30000)

        # 【★追加】スクショ撮影直前に、邪魔な広告や追従バナーを強制排除する魔法のスクリプト
        print("画面上の広告および追従バナーを非表示にしています...")
        page.evaluate("""
            // ① 広告の温床である「iframe」要素をすべてページから削除
            document.querySelectorAll('iframe').forEach(iframe => iframe.remove());
            
            // ② 画面をスクロールしてもついてくる邪魔な追従バナー（fixed, sticky）をすべて透明化
            document.querySelectorAll('*').forEach(el => {
                const style = window.getComputedStyle(el);
                if (style.position === 'fixed' || style.position === 'sticky') {
                    el.style.display = 'none';
                }
            });
        """)
        
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
