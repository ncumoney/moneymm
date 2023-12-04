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
user_status={}
    
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
    try:
        price = int(event.message.text) #ok       
        handle_message2(event.message.text) #跳quick
        category=catogery(event)
        total = count(user_id,category,price)
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=f"結果是: {price},總花費: {total}"))#這裡會用到嗎？
      
    except ValueError:
        
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text="請輸入有效的數字"))
    


def count(user_id, category, data): ##data=使用者輸入的金額 category==類別
    scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']
    creds = ServiceAccountCredentials.from_json_keyfile_name('steam-boulevard-405907-f1cc6b42920f.json', scope)
    client = gspread.authorize(creds)
    spreadsheet_name = "ncummmoney"
    sheet = client.open(spreadsheet_name)
    worksheet_titles = [worksheet.title for worksheet in sheet.worksheets()]
    worksheet_name_to_check = str(user_id)

    if worksheet_name_to_check in worksheet_titles:
        personsheet=sheet.worksheet(worksheet_name_to_check)
    else:
        personsheet = sheet.add_worksheet(title=worksheet_name_to_check, rows="1000", cols="1000")

    personsheet.append_row([category, data])
    allcount =personsheet.col_values(2)
    totocount = sum(float(value) for value in allcount if value)

    maxxx=len(personsheet.col_values(1))
    records = personsheet.col_values(1)

    countall={}
    for i in range(maxxx):
      if records[i]=='日用品':
        readwhere=int(personsheet.cell(i+1, 2).value)
        if '日用品' in countall:
          countall['日用品']+=readwhere
        else:
          countall['日用品']=readwhere
        print(countall)
      if records[i]=='娛樂':
        readwhere=int(personsheet.cell(i+1, 2).value)
        if '娛樂' in countall:
          countall['娛樂']+=readwhere
        else:
          countall['娛樂']=readwhere
        print(countall)
      if records[i]=='交通':
        readwhere=int(personsheet.cell(i+1, 2).value)
        if '交通' in countall:
          countall['交通']+=readwhere
        else:
          countall['交通']=readwhere
        print(countall)
      if records[i]=='飲食':
        readwhere=int(personsheet.cell(i+1, 2).value)
        if '飲食' in countall:
          countall['飲食']+=readwhere
        else:
          countall['飲食']=readwhere
        print(countall)
    countall['餘額']=totocount

    return countall

# handle text message
@line_handler.add(MessageEvent, message=TextMessage)
#快速選單
def handle_message2(event):  
    msg = event.message.text
    user_id = event.source.user_id
    try:
        money = int(event.message.text) #ok
        user_status[user_id]=money
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
        category=catogery(event,price)
        price=user_status[user_id]
        print(price,category)
        category_totals = count(user_id,category,price)
        print(category_totals)
        reply_message = "各類別消費總額:\n" + "\n".join([f"{category}: {total}" for category, total in category_totals.items()])
        print(reply_message)
        if total>=1000:
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text=f"這個月花太多了喔～你是大盤子嗎？已將消費{price}元分類為{category},總花費: {total}"))
        else: 
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text=f"已將消費{price}元分類為{category},總花費: {total}"))
            


# Handle PostbackEvent
@line_handler.add(PostbackEvent)
def handle_message(event):
    data = event.postback.data
    if data == 'date_postback':
        line_bot_api.reply_message(
            event.reply_token, TextSendMessage(text=event.postback.params['date']))

#@line_handler.add(MessageEvent, message=TextMessage)
#分類
def catogery(event,price):
    user_message = event.message.text
    variable_value = None

    if '飲食' in user_message.lower():
        variable_value = '飲食'
        price = -price
    elif '娛樂' in user_message.lower():
        variable_value = '娛樂'
        price = -price
    elif '交通' in user_message.lower():
        variable_value = '交通'
        price = -price
    elif '日用品' in user_message.lower():
        variable_value = '日用品'
        price = -price

    return variable_value,price

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
   