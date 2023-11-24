import os

from linebot.models import *
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from flask import Flask, request, abort, render_template


app = Flask(__name__)

Channel_Access_Token = 'IjD9cOGGINHUXelSEl+HdVAc9oEDw3/kk+XMkfWyGZCdFyURygI18eD4rKfcpaKxajwsLmA0iCwnedwrM/qPSCy5BcBNNw+z8xIx/k4ytwxrAABJspIvWUUTWEYZOnYGRUUtw1B9Ez2tyL9qhqWhcwdB04t89/1O/w1cDnyilFU='
line_bot_api    = LineBotApi(Channel_Access_Token)
Channel_Secret  = '6e4d6c59b5cd885348d5e5cc71a4957b'
handler = WebhookHandler(Channel_Secret)


# handle request from "/callback" 
@app.route("/callback", methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']
    body      = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return 'OK'


# handle text message
@handler.add(MessageEvent, message=TextMessage)
def handle_message2(event):
    msg = event.message.text

    if '金額' in msg:
        line_bot_api.reply_message(
            event.reply_token,
            flex_message=TextSendMessage(
                text='類別',
                quick_reply=QuickReply(
                    items=[
                        QuickReplyButton(
                            action=MessageAction(label="飲食", text="飲食")
                        ),
                        QuickReplyButton(
                            action=MessageAction(label="娛樂", text="娛樂")
                        ),
                        # return a location message
                        QuickReplyButton(
                            action=MessageAction(label="交通", text="交通")
                        ),
                        QuickReplyButton(
                            action=MessageAction(label="日用品", text="日用品")
                        )
                    ])))
    else:
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=msg)
        )


# Handle PostbackEvent
@handler.add(PostbackEvent)
def handle_message3(event):
    data = event.postback.data
    if data == 'date_postback':
        line_bot_api.reply_message(
            event.reply_token, TextSendMessage(text=event.postback.params['date']))


if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)