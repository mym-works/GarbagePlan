import json
import os
import database
import calc
import post
import logging
from time import sleep

logger = logging.getLogger()
logger.setLevel(logging.INFO)


def main(event, context):
    # ハウス名とLINE GroupIDを取得
    house_items = database.items_scan('borderles-line-groupid')

    # 各ハウスのゴミ捨ての担当とゴミ種類を通知
    for item in house_items:
        house_name = item['House']
        line_groupid = item['GroupId']

        # House memeberを取得
        house_info = database.items_read(
            'borderless-house-members', house_name)
        # logger.info(house_info)

        # ごみ捨て当番を取得
        # 配列の最初の二人が担当
        # 存在しなかった場合は次の部屋番号
        people_in_charge = database.items_read(
            'borderles-people-in-charge', house_name)
        people_in_charge_queue = people_in_charge[0]['Room']
        # logger.info(people_in_charge_queue)

        # 当日のごみ捨て当番を探索
        todays_people_in_charge, new_people_in_charge_queue = calc.get_todays_people_in_charge(
            house_info, people_in_charge_queue)
        logger.info(todays_people_in_charge)
        logger.info(new_people_in_charge_queue)

        # ハウスに存在するゴミの種類を取得
        type_of_garbage = database.items_read(
            'borderless-type-of-garbage', house_name)
        # logger.info(type_of_garbage)

        # 当日捨てるゴミの種類を取得
        todays_garbage_name = calc.get_todays_garbage_type(type_of_garbage)
        logger.info(todays_garbage_name)

        # ゴミの種類の配列が空ではない場合
        if todays_garbage_name:
            # 担当者を通知
            send_message = calc.make_flex_message_charge(
                line_groupid, todays_people_in_charge)
            post.line(send_message)

            sleep(1)

            # ゴミの種類を通知
            send_message = calc.make_flex_message_garbage(
                line_groupid, todays_garbage_name)
            post.line(send_message)


"""

    # ゴミの種類の配列が空ではない場合
    if todays_garbage_name:

        # 一旦今週のごみ捨て当番のレコードを削除する
        database.items_delete(
            'borderles-this-week-garbage-charge', database_charge_room_array)

        # 来週のごみ捨て当番のレコードを登録する
        database.items_add('borderles-this-week-garbage-charge',
                           'C5ac0fe9390c99fe1e7aa307168695d04', next_room, next_name)
"""
