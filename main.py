from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import *
from linebot.models import MessageEvent, TextMessage, TextSendMessage
import logging
import os
import gspread
from oauth2client.service_account import ServiceAccountCredentials


line_bot_api = LineBotApi("IjD9cOGGINHUXelSEl+HdVAc9oEDw3/kk+XMkfWyGZCdFyURygI18eD4rKfcpaKxajwsLmA0iCwnedwrM/qPSCy5BcBNNw+z8xIx/k4ytwxrAABJspIvWUUTWEYZOnYGRUUtw1B9Ez2tyL9qhqWhcwdB04t89/1O/w1cDnyilFU=")
line_handler = WebhookHandler("b7d573ed2e48da0d263982523bb3d478")
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
    app.logger.info("Request body: " + body)
    print(f"callback {body}")
    # handle webhook body
    try:
        line_handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return 'OK'

data=0
@line_handler.add(MessageEvent, message=TextMessage)
def handle_message1(event):
    user_message = event.message.text
    user_id = event.source.user_id
    print(f"text: {user_message}, user_id: {event.source.user_id}")
    print(type(event.message.text))
    print("000000000")
    print(type(event))
    try:
        price = int(event.message.text) #ok
        
        handle_message2(event.message.text) #跳quick
        print("GG@@@@@@@@")
        category=catogery(event)
        total = count(user_id,category,price)
        print(total)
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=f"結果是: {price},總花費: {total}"))
      
    except ValueError:
        
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text="請輸入有效的數字"))
    


def count(category, data): ##data=使用者輸入的金額 category==類別
    # 定義認證範圍
    scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']
    # 添加您的 JSON 憑證文件
    creds = ServiceAccountCredentials.from_json_keyfile_name('steam-boulevard-405907-f1cc6b42920f.json', scope)
    # 授權和建立客戶端
    client = gspread.authorize(creds)
    spreadsheet_name = "ncummmoney"
    # 打開 spreadsheet
    sheet = client.open(spreadsheet_name).sheet1
    print([category, data])

    # 插入數據
    sheet.append_row([category, data])
    allcount =sheet.col_values(2)
    print(allcount)
    totocount = int(sum(float(value) for value in allcount if value))
    print(totocount)

    return totocount

# handle text message
@line_handler.add(MessageEvent, message=TextMessage)
#快速選單
def handle_message2(event): 
     
    msg = event.message.text
    print(event.message.text)
    price = 0
    print("handle message2")
    try:
        money = int(event.message.text) #ok
        price = money
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(
                text='請選擇類別',
                quick_reply=QuickReply(
                    items=[
                        QuickReplyButton(
                            action=MessageAction(label="娛樂", text="娛樂")
                        ),
                        QuickReplyButton(
                            action=MessageAction(label="飲食", text="飲食")
                        ),
                        QuickReplyButton(
                            action=MessageAction(label="交通", text="交通")
                        ),
                        QuickReplyButton(
                            action=MessageAction(label="日用品", text="日用品")
                        )
                    ])))
    except ValueError:
        category=catogery(event)
        user_id = event.source.user_id
        print(user_id)
        total = count(user_id,category,price)
        print(total)
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=f"結果是: {price},總花費: {total}"))
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text="回去排隊"))


# Handle PostbackEvent
@line_handler.add(PostbackEvent)
def handle_message(event):
    data = event.postback.data
    if data == 'date_postback':
        line_bot_api.reply_message(
            event.reply_token, TextSendMessage(text=event.postback.params['date']))

#@line_handler.add(MessageEvent, message=TextMessage)
#分類
def catogery(event):
    # 獲取收到的訊息
    user_message = event.message.text

    # 初始化變數值
    variable_value = None

    # 根據收到的訊息中的關鍵字設定變數值
    if '飲食' in user_message.lower():
        variable_value = '飲食'
    elif '娛樂' in user_message.lower():
        variable_value = '娛樂'
    elif '交通' in user_message.lower():
        variable_value = '交通'
    elif '日用品' in user_message.lower():
        variable_value = '日用品'

    # 準備回覆訊息
    if variable_value is not None:
        response = f'已將該消費分類為： {variable_value}'
    else:
        response = '抱歉，我不確定您提到的是什麼。'

    # 回覆訊息
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=response)
    )
    return variable_value

#主函式
if __name__ == "__main__":

    # Spreadsheet 名稱
    spreadsheet_name = "ncummmoney"
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
    # Configure the logging
    logging.basicConfig(level=logging.INFO)

    # Log statement
    logging.info("This is a log message.")
    app.run()
   