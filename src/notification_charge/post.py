import os
import json
import requests
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)


def line(send_message):
    access_token = os.environ['ACCESS_TOKEN']

    url = 'https://api.line.me/v2/bot/message/push'
    headers = {'Content-Type': 'application/json',
               'Authorization': 'Bearer ' + access_token}

    # PythonオブジェクトをJSONに変換する
    json_data = json.dumps(send_message).encode('utf-8')

    # httpのPOSTリクエスト
    response = requests.post(
        url,
        data=json_data,
        headers=headers
    )
    logger.info(response.json())
