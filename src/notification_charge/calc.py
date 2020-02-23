import json
import datetime
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)


def get_todays_people_in_charge(house_info, people_in_charge_queue):
    todays_people_in_charge = {}
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
            todays_people_in_charge[candidate_room] = tenant_name
            pair_count += 1

        # キューを更新する
        new_people_in_charge_queue.remove(candidate_room)
        new_people_in_charge_queue.append(candidate_room)

    return todays_people_in_charge, new_people_in_charge_queue


def get_todays_garbage_type(type_of_garbage):
    print(type_of_garbage)
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
                todays_garbage_name.append(garbage_day)

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


# 新しいUIの担当者メッセージを整形する
def make_flex_message_charge(line_groupid, todays_people_in_charge):
    file = open('./conf/message_template_charge.json')
    message_template_dict = json.load(file)

    # line_groupidを代入
    message_template_dict["to"] = line_groupid

    body_dict = message_template_dict["messages"][0]["contents"]["contents"][0]["body"]["contents"]

    # 日付を代入
    today_date = datetime.datetime.today().strftime("%Y/%m/%d")
    body_dict[0]["contents"][0]["text"] = today_date

    # 担当者を代入
    rooms = list(todays_people_in_charge.keys())
    names = list(todays_people_in_charge.values())

    body_dict[2]["contents"][0]["contents"][0]["contents"][0]["text"] = rooms[0]
    body_dict[2]["contents"][0]["contents"][1]["contents"][0]["text"] = names[0]
    body_dict[3]["contents"][0]["contents"][0]["contents"][0]["text"] = rooms[1]
    body_dict[3]["contents"][0]["contents"][1]["contents"][0]["text"] = names[1]

    return message_template_dict


# 新しいUIのゴミの種類メッセージを整形する
def make_flex_message_garbage(line_groupid, todays_garbage_name):
    file = open('./conf/component_type_of_garbage.json')
    garbage_component_dict = json.load(file)

    start_json_str = '{"to":"' + line_groupid + \
        '","messages":[{"type":"flex","altText": "【Garbage Plan】","contents":{"type":"carousel","contents":['
    end_json_str = ']}}]}'

    message_template_json = start_json_str

    count = 1
    for garbage_item in todays_garbage_name:
        # 日本語を代入
        garbage_component_dict["body"]["contents"][0]["contents"][0]["contents"][0]["text"] = garbage_item["JpaneseName"]
        # 英語を代入
        garbage_component_dict["body"]["contents"][1]["text"] = garbage_item["GarbageType"]
        # URLを代入
        garbage_component_dict["hero"]["url"] = garbage_item["url"]

        message_template_json += json.dumps(garbage_component_dict)
        if count < len(todays_garbage_name):
            message_template_json += ','
        count += 1
    message_template_json += end_json_str

    message_template_dict = json.loads(message_template_json)
    return message_template_dict
