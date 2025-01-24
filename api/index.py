
import os
import sys
# from argparse import ArgumentParser

from flask import Flask, request, abort
from linebot import (
    WebhookParser
)
from linebot.v3.exceptions import (
    InvalidSignatureError
)
from linebot.v3.webhooks import (
    MessageEvent,
    TextMessageContent,
)
from linebot.v3.messaging import (
    Configuration,
    ApiClient,
    MessagingApi,
    ReplyMessageRequest,
    TextMessage
)
from api.chatgpt import ChatGPT


app = Flask(__name__)
chatgpt = ChatGPT()

# get channel_secret and channel_access_token from your environment variable
channel_secret = os.getenv('LINE_CHANNEL_SECRET', None)
channel_access_token = os.getenv('LINE_CHANNEL_ACCESS_TOKEN', None)
if channel_secret is None:
    print('Specify LINE_CHANNEL_SECRET as environment variable.')
    sys.exit(1)
if channel_access_token is None:
    print('Specify LINE_CHANNEL_ACCESS_TOKEN as environment variable.')
    sys.exit(1)

parser = WebhookParser(channel_secret)

configuration = Configuration(
    access_token=channel_access_token
)


@app.route("/", methods=['GET'])
def hello():

    # handle webhook body
    try:
        return "Hello OPENAI !!"
    except InvalidSignatureError:
        abort(400)

    return 'OK'

@app.route("/webhook", methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # parse webhook body
    try:
        events = parser.parse(body, signature)
    except InvalidSignatureError:
        abort(400)
    

    # if event is MessageEvent and message is TextMessage, then echo text
    app.logger.info("before event: %s" , len(events))
    
    for event in events:
        app.logger.info("event type: %s" , type(event))
        # if not isinstance(event, MessageEvent):
        #     continue
        # if not isinstance(event.message, TextMessageContent):
        #     continue
        app.logger.info("process api")
        with ApiClient(configuration) as api_client:
    
            if event.message.type != "text":
                return
            
            # if event.message.text == "啟動":
            #     working_status = True
            #     line_bot_api.reply_message_with_http_info(
            #                         ReplyMessageRequest(
            #         reply_token=event.reply_token,
            #         messages=[TextMessage(text="Hi 我是萬能的Crystal，歡迎來跟我互動~~")]
            #     ))
            #     return

            # if event.message.text == "安靜":
            #     working_status = False
            #     line_bot_api.reply_message(
            #         event.reply_token,
            #         TextSendMessage(text="感謝您的使用，若需要我的服務，請跟我說 「啟動」 謝謝~"))
            #     return
            
            # if working_status:
            chatgpt.add_msg(f"Human:{event.message.text}?\n")
            reply_msg = chatgpt.get_response().replace("AI:", "", 1)
            chatgpt.add_msg(f"AI:{reply_msg}\n")
            app.logger.info("process api response: %s", reply_msg)

            line_bot_api = MessagingApi(api_client)
            line_bot_api.reply_message(
                ReplyMessageRequest(
                    reply_token=event.reply_token,
                    messages=[TextMessage(text=reply_msg)]
                )
            )

    return 'OK'

   

if __name__ == "__main__":
    app.run()
