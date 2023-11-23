from cgitb import handler
import json
from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import logging
import os

line_bot_api = LineBotApi("IjD9cOGGINHUXelSEl+HdVAc9oEDw3/kk+XMkfWyGZCdFyURygI18eD4rKfcpaKxajwsLmA0iCwnedwrM/qPSCy5BcBNNw+z8xIx/k4ytwxrAABJspIvWUUTWEYZOnYGRUUtw1B9Ez2tyL9qhqWhcwdB04t89/1O/w1cDnyilFU=")
line_handler = WebhookHandler("6e4d6c59b5cd885348d5e5cc71a4957b")
working_status = os.getenv("DEFALUT_TALKING", default = "true").lower() == "true"

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
    
app = Flask(__name__)

# domain root
@app.route('/')
def home():
    logger.info("from logger print Hello, World")
    print('print Hello, World!')
    return 'Hello, World!'

@app.route("/webhook", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']
    # get request body as text
    body = request.get_data(as_text=True)
    json_data = new_func(body)
    app.logger.info("Request body: " + body)
    print(f"callback {body}")
    # handle webhook body

    try:
        line_handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    
    signature = request.headers['X-Line-Signature']
    handler.handle(body, signature)
    
    tk = json_data['events'][0]['replyToken']         # 取得 reply token
    msg = json_data['events'][0]['message']['text']   # 取得使用者發送的訊息

    try:
        data = int(msg)
        print("訊息成功轉換為整數:", data)
        category="飲食" ##測試而已可刪==使用者輸入的類別
        # Spreadsheet 名稱
        spreadsheet_name = "ncummmoney" ###要放到main

        # 呼叫函數添加數據
        
        totalcount = count(spreadsheet_name, category, data)
    except ValueError:
        print("訊息無法轉換成整數")
    
    text_message = TextSendMessage(text=msg)          # 設定回傳同樣的訊息
    line_bot_api.reply_message(tk,text_message)       # 回傳訊息
    return 'OK'

def new_func(body):
    return json.loads(body)

@line_handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    user_message = event.message.text
    print(f"text: {user_message}, user_id: {event.source.user_id}")
    
    reply_message = TextSendMessage(text=user_message)
    line_bot_api.reply_message(event.reply_token, reply_message)
    return

def count(spreadsheet_name, category, data): ##data=使用者輸入的金額 category==類別
    # 定義認證範圍
    scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']
    # 添加您的 JSON 憑證文件
    creds = ServiceAccountCredentials.from_json_keyfile_name(r'C:\Users\yunyu\Desktop\moneymm\steam-boulevard-405907-f1cc6b42920f.json', scope)
    # 授權和建立客戶端
    client = gspread.authorize(creds)
    # 打開 spreadsheet
    sheet = client.open(spreadsheet_name).sheet1

    # 插入數據
    sheet.append_row([category, data])
    allcount =sheet.col_values(2)
    totocount = sum(float(value) for value in allcount if value)

    return totocount

if __name__ == "__main__":
    totalcount =0
    # Configure the logging
    logging.basicConfig(level=logging.INFO)

    # Log statement
    logging.info("This is a log message.")
    app.run()