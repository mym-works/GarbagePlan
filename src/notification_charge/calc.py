import json
import datetime
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)


def get_todays_people_in_charge(house_info, people_in_charge_queue):
    todays_people_in_charge = []
    new_people_in_charge_queue = people_in_charge_queue.copy()

    pair_count = 0
    for candidate_room in people_in_charge_queue:
        # ペアになったらループを抜ける
        if 2 <= pair_count:
            break

        # ハウスメイトの情報から入居者の名前を取り出す
        tenant_names = [x['Name']
                        for x in house_info if x['Room'] == candidate_room]
        tenant_name = tenant_names[0]

        # ハウスメイトが住んでいる場合
        if tenant_name != 'None':
            todays_people_in_charge.append({candidate_room: tenant_name})
            pair_count += 1

        # キューを更新する
        new_people_in_charge_queue.remove(candidate_room)
        new_people_in_charge_queue.append(candidate_room)

    print(todays_people_in_charge)
    print(new_people_in_charge_queue)
    return todays_people_in_charge, new_people_in_charge_queue


def get_todays_garbage_type(type_of_garbage):
    week_day_array = ["Monday", "Tuesday", "Wednesday",
                      "Thursday", "Friday", "Saturday", "Sunday"]
    today_time = datetime.datetime.now()
    weekday_num = today_time.weekday() + 1
    # 曜日が漏れたら初期化
    if weekday_num >= 7:
        weekday_num = 0

    todays_day = week_day_array[weekday_num]

    todays_garbage_name = []
    for garbage_day in type_of_garbage:
        for day in garbage_day["Day"]:
            if todays_day == day:
                todays_garbage_name.append(garbage_day["GarbageType"])
    logger.info(todays_day)
    logger.info(todays_garbage_name)

    return todays_garbage_name


# ゴミ捨て当番の送るメッセージを整形
def make_garbage_massege(names, rooms, todays_garbage_name):
    send_message = ""
    for (name, room) in zip(names, rooms):
        send_message += room + " " + name + "\n"

    send_message += "\nWould you please throw out the following garbage\n"

    for garbage_name in todays_garbage_name:
        send_message += "* " + garbage_name + "\n"

    return send_message
