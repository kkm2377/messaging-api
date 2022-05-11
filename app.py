import os
import sys
import requests
from flask import Flask, request, abort
from PIL import Image
from io import BytesIO

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage, ImageMessage,
)

app = Flask(__name__)

# 環境変数からchannel_secret・channel_access_tokenを取得
channel_secret = "73727f04bacc676d96039269aa2b5f18"
channel_access_token = "IqkMy4nU1YEDh8uujEBAGc4hXjIrGQwnsxGZRXpQE6Ytw7dtfVLsUl/X8adr8tEM1LHEmzK2VxEha8A6K4arHQL2qgfaCUOKiM+AJbQG/A5ZmG2w7gL3GYVTzYQDB2s3xpDnvXmWogWeTjjR6wHI7QdB04t89/1O/w1cDnyilFU="

if channel_secret is None:
    print('Specify LINE_CHANNEL_SECRET as environment variable.')
    sys.exit(1)
if channel_access_token is None:
    print('Specify LINE_CHANNEL_ACCESS_TOKEN as environment variable.')
    sys.exit(1)


line_bot_api = LineBotApi(channel_access_token)
handler = WebhookHandler(channel_secret)

@app.route("/")
def hello_world():
    return "hello world!"

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
        abort(400)

    return 'OK'


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=event.message.text))

@handler.add(MessageEvent, message=ImageMessage)
def handle_message(event):
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=event.message.id))


if __name__ == "__main__":
    app.run()
