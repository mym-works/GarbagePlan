import json
import datetime
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)


def confirm_charge(room_members, this_week_charger):
    room_number_array = []
    room_name_array = []
    for member in room_members:
        room_number_array.append(member["Room"])
        room_name_array.append(member["Name"])

    charge_room_array = []
    charge_name_array = []
    for charger in this_week_charger:
        charge_room_array.append(charger["Room"])
        charge_name_array.append(charger["Name"])

    confirm_index = []
    confirm_flag = []
    for (name, room) in zip(charge_name_array, room_number_array):
        name = name.rstrip()
        room = room.rstrip()
        try:
            index = room_name_array.index(name)
            confirm_index.append(index)
            confirm_flag.append(True)
        except ValueError:
            index = room_number_array.index(room)
            confirm_index.append(index + 2)
            confirm_flag.append(False)

    logger.info(confirm_index)
    logger.info(confirm_flag)

    # 当番の名前がいるか比較する
    print(confirm_flag)
    correc_room = []
    correc_name = []
    if confirm_flag == [True, True]:
        for index in confirm_index:
            correc_name.append(room_number_array[index])
            correc_room.append(room_name_array[index])
    elif confirm_flag == [True, False]:
        pass
    elif confirm_flag == [False, True]:
        pass
    else:
        pass

    return correc_room, correc_name


def confirm_garbage_type(type_of_garbage):
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
