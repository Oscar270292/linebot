from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
)

app = Flask(__name__)

line_bot_api = LineBotApi('ereMlZqxLxLLbz9QZAdW9D7Epo6tEI0PjgP5S+wqua+qKRwwQO8hsRZZI70l8SL0hs0UpMPTy20OnC8eucfHIWHm3Y5Ln/HZI4sRRb4EGodSQ0ejtts9qfg8fFrkKngIDhR9EN7sEBam84qHj/BwcgdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('060c239d6a80db3b02a387e1dcb1e0f6')


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
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=event.message.text))


if __name__ == "__main__":
    app.run()