from flask import Flask, request, abort
from linebot import LineBotApi
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage
from api.chatgpt import ChatGPT
from linebot import (
    WebhookParser
)

import os

line_bot_api = LineBotApi(os.getenv("LINE_CHANNEL_ACCESS_TOKEN"))
# line_handler = WebhookHandler(os.getenv("LINE_CHANNEL_SECRET"))
parser = WebhookParser(os.getenv("LINE_CHANNEL_SECRET"))
working_status = os.getenv("DEFALUT_TALKING", default = "true").lower() == "true"

app = Flask(__name__)
chatgpt = ChatGPT()

# domain root
@app.route('/')
def home():
    return 'Hello, World!'

@app.route("/webhook", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']
    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)
    # handle webhook body
    try:
        events = parser.parse(body, signature)
    except InvalidSignatureError:
        abort(400)
    return 'OK'

    # if event is MessageEvent and message is TextMessage, then echo text
    app.logger.info("before event: %s" , len(events))
    for event in events:
        app.logger.info("event type: %s" , type(event))
        # if not isinstance(event, MessageEvent):
        #     continue
        # if not isinstance(event.message, TextMessageContent):
        #     continue
        app.logger.info("process api")

    
        if event.message.type != "text":
            return
        
        if event.message.text == "啟動":
            working_status = True
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text="我是時下流行的AI智能，目前可以為您服務囉，歡迎來跟我互動~"))
            return

        if event.message.text == "安靜":
            working_status = False
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text="感謝您的使用，若需要我的服務，請跟我說 「啟動」 謝謝~"))
            return
        
        if working_status:
            chatgpt.add_msg(f"Human:{event.message.text}?\n")
            reply_msg = chatgpt.get_response().replace("AI:", "", 1)
            chatgpt.add_msg(f"AI:{reply_msg}\n")
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text=reply_msg))


   

if __name__ == "__main__":
    app.run()
