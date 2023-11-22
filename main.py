from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage
import json
import os

line_bot_api = LineBotApi("IjD9cOGGINHUXelSEl+HdVAc9oEDw3/kk+XMkfWyGZCdFyURygI18eD4rKfcpaKxajwsLmA0iCwnedwrM/qPSCy5BcBNNw+z8xIx/k4ytwxrAABJspIvWUUTWEYZOnYGRUUtw1B9Ez2tyL9qhqWhcwdB04t89/1O/w1cDnyilFU=")
line_handler = WebhookHandler("6e4d6c59b5cd885348d5e5cc71a4957b")

app = Flask(__name__)

@app.route('/')
def home():
    return 'Hello, World!'

@app.route("/webhook", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']
    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)
    # handle webhook body
    try:
        line_handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return 'OK'


@line_handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    if event.message.type != "text":
        return

    line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text="我可以說話囉，歡迎來跟我互動 ^_^ "))
    return

def callback1():
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
        text_message = TextSendMessage(text=msg)          # 設定回傳同樣的訊息
        line_bot_api.reply_message(tk,text_message)       # 回傳訊息
    except:
        print('error')
    return 'OK'

if __name__ == "__main__":
    app.run()
