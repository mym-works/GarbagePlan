import urllib.request
import json
import os
import database
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)


def line_bot_response(event, context):
    response = database.member_read()
    room_member = response["Items"]
    logger.info(room_member)

    response = database.this_week_charger()
    this_week_charger = response["Items"]
    logger.info(this_week_charger)

    # post_to_line()


def post_to_line():
    access_token = os.environ['ACCESS_TOKEN']
    group_id = os.environ['GROUP_ID']

    url = "https://api.line.me/v2/bot/message/push"
    method = "POST"
    headers = {"Content-Type": "application/json",
               "Authorization": 'Bearer ' + access_token}

    # PythonオブジェクトをJSONに変換する
    obj = {
        'to': group_id,
        'messages': [{
            'type': 'text',
            'text': "こんにちは",
        }],
    }
    json_data = json.dumps(obj).encode("utf-8")

    # httpリクエストを準備してPOST
    request = urllib.request.Request(
        url, data=json_data, method=method, headers=headers)
    with urllib.request.urlopen(request) as response:
        response_body = response.read().decode("utf-8")
