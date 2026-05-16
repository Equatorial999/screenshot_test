import requests
import json

def run():
    # ★★★ここにGASのウェブアプリURLを貼り付けてください★★★
    gas_url = "https://script.google.com/macros/s/AKfycbz2wxOTjdAaB2LUSqvn33dEjGF909ANLSb4gxL0EBxhHlJAR88d7bSHDOxAckozCsVC/exec"
    
    # 送信するシンプルなテストデータ
    payload = {
        "message": "これはGitHub Actionsから送信された、部品1の接続テスト用テキストです。",
        "fileName": "github_test_connection.txt"
    }
    
    print("GAS（Googleドライブ）へテストデータを送信しています...")
    try:
        # データを送信
        response = requests.post(gas_url, json=payload)
        response.raise_for_status()
        
        # サーバーからの返答（JSON）を解析
        result = response.json()
        if result.get("status") == "success":
            print("【大成功】Googleドライブへのファイル保存が確認されました！")
            print(f"作成されたファイルのURL: {result.get('url')}")
        else:
            print(f"【GAS側エラー】{result.get('message')}")
            
    except Exception as e:
        print(f"【通信エラー】発生しました: {e}")
        if 'response' in locals():
            print(f"サーバーからの生の返答内容:\n{response.text}")

if __name__ == "__main__":
    run()
