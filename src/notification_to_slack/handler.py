import requests
import json
import os
import database
import calc
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)


def main(event, context):
    room_members = database.items_read('borderless-house-members')
    logger.info(room_members)

    this_week_charger = database.items_read(
        'borderles-this-week-garbage-charge-slack')
    logger.info(this_week_charger)

    type_of_garbage = database.items_read('borderless-type-of-garbage')
    logger.info(type_of_garbage)

    # 今週のゴミ当番がいるか確認
    database_charge_room_array, correc_room, correc_name, next_room, next_name = calc.confirm_charge(
        room_members, this_week_charger)

    # ゴミの種類を取得
    todays_garbage_name = calc.confirm_garbage_type(type_of_garbage)

    # ゴミの種類の配列が空ではない場合
    if todays_garbage_name:
        # メッセージを整形
        send_message = calc.make_garbage_massege(
            correc_name, correc_room, todays_garbage_name)
        # メッセージをSlackに送信
        post_to_slack(send_message)

        # 一旦今週のごみ捨て当番のレコードを削除する
        database.items_delete(
            'borderles-this-week-garbage-charge-slack', database_charge_room_array)

        # 来週のごみ捨て当番のレコードを登録する
        database.items_add('borderles-this-week-garbage-charge-slack',
                           'C5ac0fe9390c99fe1e7aa307168695d04', next_room, next_name)


def post_to_slack(send_message):
    url = "https://hooks.slack.com/services/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"

    payload = {
        'text': send_message
    }

    requests.post(url, data=json.dumps(payload))
