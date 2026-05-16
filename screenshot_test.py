from playwright.sync_api import sync_playwright
import time
from datetime import datetime

def extract_forward_pe(table_text, index_name):
    """テキストから特定の指数のForward PER(3番目の数値)を抜き出す関数"""
    for line in table_text.split("\n"):
        if index_name in line:
            # タブやスペースで文字を細かく分割します
            parts = line.split("\t")
            if len(parts) < 2: # タブで区切られていない場合は半角スペースで試す
                parts = [p for p in line.split(" ") if p]
            
            # 分割した結果、インデックス名以降に数値が並んでいるか確認
            # 構造：[インデックス名, 実績PER, 1年前PER, 予想PER(Forward)...]
            # インデックス名が複数単語（例：S&P 500 Index）の場合を考慮して、数値部分の後ろから数えます
            try:
                # ログの構造から、DIV YIELDの手前までの数値（左から3番目の数値）を特定します
                # 今回のログの並び：[インデックス名, 当日実績, 1年前実績, 予想(Forward), 当日利回り, 1年前利回り]
                # つまり、インデックス名を除いた数値リストの「3番目（インデックス2）」がForward PEです
                
                # 数値らしき要素（ドットを含むものなど）だけを抽出
                numeric_parts = [p for p in parts if any(char.isdigit() for char in p) and "." in p]
                if len(numeric_parts) >= 3:
                    return numeric_parts[2] # 3番目の数値を返す
            except Exception as e:
                return f"抽出エラー: {e}"
    return "見つかりませんでした"

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
        
        # すべての表のテキストを合体させる
        all_tables_text = ""
        tables = page.locator("table").all()
        for table in tables:
            all_tables_text += table.inner_text() + "\n"
        
        # 今日の日付を取得 (YYYY/MM/DD)
        today_str = datetime.now().strftime("%Y/%m/%d")
        
        # 各指数のForward PERをピンポイントで抽出
        dow_pe = extract_forward_pe(all_tables_text, "Dow Jones Industrial Average")
        nasdaq_pe = extract_forward_pe(all_tables_text, "NASDAQ 100 Index")
        sp500_pe = extract_forward_pe(all_tables_text, "S&P 500 Index")
        
        print("\n▼▼▼ 抽出結果（スプレッドシートに記録する予定のデータ） ▼▼▼")
        print(f"記録日: {today_str}")
        print(f"ダウ平均 (Dow Jones) : {dow_pe}")
        print(f"ナスダック (NASDAQ 100) : {nasdaq_pe}")
        print(f"S&P 500 : {sp500_pe}")
        print("▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲\n")
        
        page.screenshot(path="wsj_screenshot.png", full_page=True)
        print("スクリーンショットの撮影に成功しました！")
        
        browser.close()

if __name__ == "__main__":
    run()
