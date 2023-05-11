import os
from datetime import datetime, timedelta

from dateutil import parser
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError

# Slack APIトークンを設定してください
client = WebClient(token=os.environ['SLACK_BOT_TOKEN'])

# 1年前の日付を設定します
cutoff_date = datetime.today() - timedelta(days=180)

try:
    # WebClientを使用してconversations.listメソッドを呼び出し、チャンネルのリストを取得します
    channels_list_response = client.conversations_list(types="public_channel", exclude_archived=True, limit=1000)

    for channel in channels_list_response['channels']:
        # チャンネルの最後に投稿されたメッセージを取得します
        conversation_history = client.conversations_history(channel=channel['id'])
        if conversation_history['messages']:
            last_message = conversation_history['messages'][0]
            last_message_date = datetime.fromtimestamp(float(last_message['ts']))
            # 最後に投稿されたメッセージが1年以上前かどうかを確認します
            if last_message_date < cutoff_date:
                userName = last_message['user']
                print(f"チャンネル {channel['name']} は半年以上更新されていません.user={userName}")
        else:
            # チャンネルにメッセージがない場合は、チャンネルの作成日時を確認します
            channel_info = client.conversations_info(channel=channel['id'])
            channel_creation_date = datetime.fromtimestamp(float(channel_info['channel']['created']))
            # チャンネルが1年以上前に作成されたかどうかを確認します
            if channel_creation_date < cutoff_date:
                print(f"チャンネル {channel['name']} は半年以上更新されていません")
except SlackApiError as e:
    print("Error: {}".format(e))
