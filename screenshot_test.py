import requests

def run():
    # ★★★ここにGASのウェブアプリURLを貼り付けてください★★★
    gas_url = "あなたのGASのウェブアプリURLをここに貼り付け"
    
    # 今回は合図を送るだけなので、ダミーのデータを送ります
    payload = {"test": "email_trigger"}
    
    print("GASへ『メールを送信せよ』という指示を出しています...")
    try:
        response = requests.post(gas_url, json=payload)
        response.raise_for_status()
        
        result = response.json()
        if result.get("status") == "success":
            print("【大成功】GASが指示を受け取りました！ご自身のGmailを確認してください。")
        else:
            print(f"【GAS側エラー】{result.get('message')}")
            
    except Exception as e:
        print(f"【通信エラー】発生しました: {e}")

if __name__ == "__main__":
    run()
