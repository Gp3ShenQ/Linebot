from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,StickerSendMessage
)

app = Flask(__name__)

line_bot_api = LineBotApi('IZ0RHIn1YUpkwGwOA5bM2CHPZsHokmNRkfFu2nN7k6OLquyFZcOpYC0+YcHhk+F9Hnyp5wsiBqV7pbIW3fH4bMUkH+LC1e746JIw1/EUiE1WbXuw2wkT0/wBUGLGwnG8SHSBUYwWi4ysb5Q4AkIJhwdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('550af5c7ae382eef322ee59f51a89b6f')


@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        print("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)

    return 'OK'


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    msg = event.message.text
    r = '很抱歉,您說什麼'

    if '貼圖' in msg:
        sticker_message = StickerSendMessage(
            package_id='1',
            sticker_id='1'
        )

        line_bot_api.reply_message(
        event.reply_token,
        sticker_message)

        return
        
    if msg in ['hi','Hi','HI']:
        r = '喵!!'
    elif msg == '你吃飯了嗎?' :
        r = '我可愛嗎'
    elif msg == '你是誰?':
        r = 'Uma超可愛'
    elif 'Uma' in msg:
        r = '喵!你找我喵?'

    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=r))


if __name__ == "__main__":
    app.run()