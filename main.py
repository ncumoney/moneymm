from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import *
from linebot.models import MessageEvent, TextMessage, TextSendMessage
from datetime import datetime
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

def get_current_date():
    # 獲取當前日期並格式化為 YYYY-MM
    return datetime.now().strftime('%Y-%m')

data=0
@line_handler.add(MessageEvent, message=TextMessage)
def handle_message1(event):
    user_message = event.message.text
    user_id = event.source.user_id
    try:
        price = int(event.message.text) #ok       
        handle_message2(event.message.text) #跳quick
        category=catogery(event,price)
        total = count(user_id,category,price)
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=f"結果是: {price},總花費: {total}"))#這裡會用到嗎？
      
    except ValueError:
        if user_message == '查詢消費紀錄':
            line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text="請輸入要查詢的紀錄 (YYYY-MM): ")
        )
        elif '-' in user_message.content():
            category_totals = calculate_expense(user_message,user_id,event) #這是上面那個def的（可能是我們count會改的部分）
            reply_message = f"{user_message}的各類别消費情况如下：\n"
            for allcategory, data in category_totals.items():
                if allcategory == '收入':
                    reply_message += f"收入: {data[0]}元\n"
                elif allcategory == '總花費':
                    reply_message += f"總花費: {data}元\n"
                elif allcategory == '餘額':
                    reply_message += f"餘額: {data}元\n"
                else:
                    reply_message += f"{allcategory}消費: {data[0]}元，占比: {data[1]}%\n"
                line_bot_api.reply_message(
                    event.reply_token,
                    TextSendMessage(text=reply_message)
                )
        else:
           line_bot_api.reply_message(
                    event.reply_token,
                    TextSendMessage(text="請輸入有效數字。如需記帳請直接輸入數字，如需查詢紀錄請輸入'查詢消費紀錄'。")
                )
    


def count(user_id, category, data): ##data=使用者輸入的金額 category==類別
    scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']
    creds = ServiceAccountCredentials.from_json_keyfile_name('steam-boulevard-405907-f1cc6b42920f.json', scope)
    client = gspread.authorize(creds)
    spreadsheet_name = "ncummmoney"
    sheet = client.open(spreadsheet_name)
    current_date = get_current_date() 
    worksheet_titles = [worksheet.title for worksheet in sheet.worksheets()]
    worksheet_name_to_check = str(user_id)

    if worksheet_name_to_check in worksheet_titles:
        personsheet=sheet.worksheet(worksheet_name_to_check)
    else:
        personsheet = sheet.add_worksheet(title=worksheet_name_to_check, rows="1000", cols="1000")

    personsheet.append_row([current_date, category, data])
    allcount =personsheet.col_values(3)
    totocount = sum(float(value) for value in allcount if value)

    maxxx=len(personsheet.col_values(2))
    records = personsheet.col_values(2)
    now_mounth = personsheet.col_values(1)

    countall={}
    for i in range(maxxx):
      if get_current_date()==now_mounth[i] :
        if records[i]=='日用品':
          readwhere=int(personsheet.cell(i+1, 3).value)
          if '日用品' in countall:
            countall['日用品'][0]+=readwhere
          else:
            countall['日用品']=[readwhere]
          print(countall)
        if records[i]=='娛樂':
          readwhere=int(personsheet.cell(i+1, 3).value)
          if '娛樂' in countall:
            countall['娛樂'][0]+=readwhere
          else:
            countall['娛樂']=[readwhere]
          print(countall)
        if records[i]=='交通':
          readwhere=int(personsheet.cell(i+1, 3).value)
          if '交通' in countall:
            countall['交通'][0]+=readwhere
          else:
            countall['交通']=[readwhere]
          print(countall)
        if records[i]=='飲食':
          readwhere=int(personsheet.cell(i+1, 3).value)
          if '飲食' in countall:
            countall['飲食'][0]+=readwhere
          else:
            countall['飲食']=[readwhere]
          print(countall)
        if records[i]=='收入':
          readwhere=int(personsheet.cell(i+1, 3).value)
          if '收入' in countall:
            countall['收入'][0]+=readwhere
          else:
            countall['收入']=[readwhere]
          print(countall)
    for category in ['飲食', '交通', '娛樂', '日用品']:
      if category not in countall:
        countall[category] = [0, 0]
    countall['總花費'] = sum(countall[cat][0] for cat in ['飲食', '交通', '娛樂', '日用品'])
    countall['餘額']=totocount
    countall['日用品'].append(round(countall['日用品'][0]/countall['總花費']*100,2))
    countall['交通'].append(round(countall['交通'][0]/countall['總花費']*100,2))
    countall['飲食'].append(round(countall['飲食'][0]/countall['總花費']*100,2))
    countall['娛樂'].append(round(countall['娛樂'][0]/countall['總花費']*100,2))

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
                        ),
                        QuickReplyButton(
                            action=MessageAction(label="收入", text="收入")
                        )
                        
                    ])))
    except ValueError:
        price=user_status[user_id]
        category,price=catogery(event,price)
        print("price,category")
        print(price,category)
        category_totals = count(user_id,category,price)
        print(category_totals)
        reply_message = "各類别消費情况如下：\n"
        for allcategory, data in category_totals.items():
            if allcategory == '收入':
                reply_message += f"收入: {data[0]}元\n"
            elif allcategory == '總花費':
                reply_message += f"總花費: {data}元\n"
            elif allcategory == '餘額':
                reply_message += f"餘額: {data}元\n"
            else:
                reply_message += f"{allcategory}消費: {data[0]}元，占比: {data[1]}%\n"
        print(reply_message)
        print(category)
        if category_totals['餘額']<=1000:
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text=f"{reply_message}\n\n這個月花太多了喔～你是大盤子嗎？\n已將{price}元分類為{category},餘額: {category_totals['餘額']}"))
        else: 
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text=f"{reply_message}\n\n已將{price}元分類為{category},總花費: {category_totals['餘額']}"))
            


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
    elif '收入' in user_message.lower():
        variable_value = '收入'
        

    return variable_value,price

#calculate_expense(user_message,user_id)
def calculate_expense(user_message,user_id,event): ##data=使用者輸入的金額 category==類別
    scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']
    creds = ServiceAccountCredentials.from_json_keyfile_name('/content/steam-boulevard-405907-f1cc6b42920f.json', scope)
    client = gspread.authorize(creds)
    spreadsheet_name = "ncummmoney"
    sheet = client.open(spreadsheet_name)
    worksheet_titles = [worksheet.title for worksheet in sheet.worksheets()]
    worksheet_name_to_check = str(user_id)

    if worksheet_name_to_check in worksheet_titles:
        personsheet=sheet.worksheet(worksheet_name_to_check)
    else:
        line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text="您沒有任何記帳紀錄")
            )
        return 0

    allcount =personsheet.col_values(3)
    totocount = sum(float(value) for value in allcount if value)

    maxxx=len(personsheet.col_values(2))
    records = personsheet.col_values(2)
    now_mounth = personsheet.col_values(1)

    countall={}
    for i in range(maxxx):
      if user_message==now_mounth[i] :
        if records[i]=='日用品':
          readwhere=int(personsheet.cell(i+1, 3).value)
          if '日用品' in countall:
            countall['日用品'][0]+=readwhere
          else:
            countall['日用品']=[readwhere]
        if records[i]=='娛樂':
          readwhere=int(personsheet.cell(i+1, 3).value)
          if '娛樂' in countall:
            countall['娛樂'][0]+=readwhere
          else:
            countall['娛樂']=[readwhere]
        if records[i]=='交通':
          readwhere=int(personsheet.cell(i+1, 3).value)
          if '交通' in countall:
            countall['交通'][0]+=readwhere
          else:
            countall['交通']=[readwhere]
        if records[i]=='飲食':
          readwhere=int(personsheet.cell(i+1, 3).value)
          if '飲食' in countall:
            countall['飲食'][0]+=readwhere
          else:
            countall['飲食']=[readwhere]
        if records[i]=='收入':
          readwhere=int(personsheet.cell(i+1, 3).value)
          if '收入' in countall:
            countall['收入'][0]+=readwhere
          else:
            countall['收入']=[readwhere]
    for category in ['飲食', '交通', '娛樂', '日用品']:
      if category not in countall:
        countall[category] = [0, 0]
    countall['總花費'] = sum(countall[cat][0] for cat in ['飲食', '交通', '娛樂', '日用品'])
    countall['餘額']=totocount
    countall['日用品'].append(round(countall['日用品'][0]/countall['總花費']*100,2))
    countall['交通'].append(round(countall['交通'][0]/countall['總花費']*100,2))
    countall['飲食'].append(round(countall['飲食'][0]/countall['總花費']*100,2))
    countall['娛樂'].append(round(countall['娛樂'][0]/countall['總花費']*100,2))

    return countall


#主函式
if __name__ == "__main__":

    # Spreadsheet 名稱
    spreadsheet_name = "ncummmoney"
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)# 例外狀況
    # Configure the logging、
    logging.basicConfig(level=logging.INFO)

    # Log statement
    logging.info("This is a log message.")
    app.run()
   