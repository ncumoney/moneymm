
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
        msg = json_data['events'][0]['message']['text']   # 取得使用者發送的訊息
        #將msg（消費金額）存入資料庫中
        text_message = TextSendMessage(text='請選擇種類')          # 設定回傳同樣的訊息
        line_bot_api.reply_message(tk,text_message)       # 回傳訊息
        #給選擇器按鈕
        
    except:
        print('若需要幫忙記帳，請輸入金額喔！')
    return 'OK'

if __name__ == "__main__":
    callback()
    app.run()
