from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage
import logging
import os
import count


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
def handle_message(event):
    user_message = event.message.text
    print(f"text: {user_message}, user_id: {event.source.user_id}")
    print("12345")
    print(type(event.message.text))
    
    
   
    
    try:
        price = int(event.message.text) #ok
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=f"結果是: {price}"))
        total = count(spreadsheet_name, category,price)
        print(total)
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=f"總花費: {total}"))
    except ValueError:
        
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text="請輸入有效的數字"))
    '''
    if "吃" in event.message.text:
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text="多少錢呢？ "))
        return
    else:
        reply_message = TextSendMessage(text=user_message)
        line_bot_api.reply_message(event.reply_token, reply_message)
    return
'''
if __name__ == "__main__":
    category="飲食" ##測試而已可刪==使用者輸入的類別
    # Spreadsheet 名稱
    spreadsheet_name = "ncummmoney"
    # Configure the logging
    logging.basicConfig(level=logging.INFO)

    # Log statement
    logging.info("This is a log message.")
    app.run()