import urllib.request
import json
import os
import database
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)


def line_bot_response(event, context):
    room_member = database.items_read('borderless-house-members')
    logger.info(room_member)

    this_week_charger = database.items_read(
        'borderles-this-week-garbage-charge')
    logger.info(this_week_charger)

    type_of_garbage = database.items_read('borderless-type-of-garbage')
    logger.info(type_of_garbage)

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
