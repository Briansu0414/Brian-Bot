from flask import Flask, request, abort


from linebot.v3 import (

    WebhookHandler
)

from linebot.v3.exceptions import (

    InvalidSignatureError
)

from linebot.v3.messaging import (

    Configuration,

    ApiClient,

    MessagingApi,

    ReplyMessageRequest,

    PushMessageRequest,

    BroadcastRequest,

    MulticastRequest,

    TextMessage
)

from linebot.v3.webhooks import (

    MessageEvent,

    TextMessageContent
)

import os

app = Flask(__name__)


configuration = Configuration(access_token=os.getenv('CHANNEL_ACCESS_TOKEN'))
line_handler = WebhookHandler(os.getenv('CHANNEL_SECRET'))


@app.route("/callback", methods=['POST'])

def callback():

    # get X-Line-Signature header value

    signature = request.headers['X-Line-Signature']


    # get request body as text

    body = request.get_data(as_text=True)

    app.logger.info("Request body: " + body)


    # handle webhook body

    try:
        line_handler.handle(body, signature)

    except InvalidSignatureError:

        app.logger.info("Invalid signature. Please check your channel access token/channel secret.")

        abort(400)


    return 'OK'



# 訊息事件

@line_handler.add(MessageEvent, message=TextMessageContent)

def message_text(event):

    with ApiClient(configuration) as api_client:

        line_bot_api = MessagingApi(api_client)
        

        # Reply message

        line_bot_api.reply_message(

            ReplyMessageRequest(

                reply_token=event.reply_token,

                messages=[TextMessage(text='理性投資')]  # 自動回覆的訊息內容
            )
        )


        # Push message (針對當前用戶)

        line_bot_api.push_message_with_http_info(

            PushMessageRequest(

                to=event.source.user_id,  # 從事件取得用戶的 ID

                messages=[TextMessage(text='PUSH!')]
            )
        )


if __name__ == "__main__":

    with ApiClient(configuration) as api_client:

        line_bot_api = MessagingApi(api_client)


        # 主動推播訊息

        line_bot_api.push_message_with_http_info(

            PushMessageRequest(

                to='Uad5f1a3daf5e695c3dbb0e802db5fb55',  # 固定的 user_id

                messages=[TextMessage(text='Hello! This is a proactive push message.')]
            )
        )
    
    app.run()