
from flask import Flask, request
from linebot import LineBotApi, WebhookHandler
from linebot.models import TextSendMessage   # 載入 TextSendMessage  模組
import json

app = Flask(__name__)

@app.route('/')
def home():
    return 'Hello, World!'

@app.route("/webhook", methods=['POST'])
def callback():
    body = request.get_data(as_text=True)
    json_data = json.loads(body)
    print(json_data)
    try:
        line_bot_api = LineBotApi('IjD9cOGGINHUXelSEl+HdVAc9oEDw3/kk+XMkfWyGZCdFyURygI18eD4rKfcpaKxajwsLmA0iCwnedwrM/qPSCy5BcBNNw+z8xIx/k4ytwxrAABJspIvWUUTWEYZOnYGRUUtw1B9Ez2tyL9qhqWhcwdB04t89/1O/w1cDnyilFU=')
        handler = WebhookHandler('6e4d6c59b5cd885348d5e5cc71a4957b')
        signature = request.headers['X-Line-Signature']
        handler.handle(body, signature)
        
        tk = json_data['events'][0]['replyToken']         # 取得 reply token
        msg = json_data['events'][0]['message']['text'] # 取得使用者發送的訊息
        replykind = "請選擇種類"
        try:
            user_input_as_int = int(msg)
            # 儲存到資料庫或進行其他操作
            # 這裡暫時只是印出轉換後的整數作為示範
            print("使用者輸入的數字:", user_input_as_int)
        except ValueError:
            print("請輸入有效的數字")

        replykind = "請選擇種類"
        text_message = TextSendMessage(text=msg)  
        text_message = TextSendMessage(text=replykind)          # 設定回傳同樣的訊息
        line_bot_api.reply_message(tk,text_message)       # 回傳訊息
    except:
        print('請輸入金額')
    return 'OK'



if __name__ == "__main__":
    callback()
    app.run()
