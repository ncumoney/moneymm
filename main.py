from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage
import logging
import os

line_bot_api = LineBotApi(os.getenv("LINE_CHANNEL_ACCESS_TOKEN"))
line_handler = WebhookHandler(os.getenv("LINE_CHANNEL_SECRET"))
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
<<<<<<< HEAD
=======
    
    signature = request.headers['X-Line-Signature']
    handler.handle(body, signature)
    
    tk = json_data['events'][0]['replyToken']         # 取得 reply token
    msg = json_data['events'][0]['message']['text']   # 取得使用者發送的訊息
    '''
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
    '''
    text_message = TextSendMessage(text=msg)          # 設定回傳同樣的訊息
    line_bot_api.reply_message(tk,text_message)       # 回傳訊息
>>>>>>> c8caeb41d0fec74d088be136c8ab55b22c4321b8
    return 'OK'


@line_handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    user_message = event.message.text
    print(f"text: {user_message}, user_id: {event.source.user_id}")

    if "吃" in event.message.text:
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text="多少錢呢？ "))
        return
    else:
        reply_message = TextSendMessage(text=user_message)
        line_bot_api.reply_message(event.reply_token, reply_message)
    return

if __name__ == "__main__":
    print("Robin Su")
    # Configure the logging
    logging.basicConfig(level=logging.INFO)

    # Log statement
    logging.info("This is a log message.")
    app.run()