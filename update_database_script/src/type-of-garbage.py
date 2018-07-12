import boto3
from boto3 import dynamodb
from boto3.session import Session
from boto3.dynamodb.conditions import Key, Attr

dynamodb_session = Session(profile_name="mayama-cli",
                           region_name="ap-northeast-1")
dynamodb = dynamodb_session.resource('dynamodb')
house_member_table = dynamodb.Table("borderless-type-of-garbage")

# ハウスの名前を入れる
house_name = "Oimachi"


def main():
    update()
    scan()


def update():
    file = open("../conf/type-of-garbage.csv", "r")

    garbage_type = []
    day = []
    for line in file:
        items = line.split(",")
        garbage_type.append(items[0])
        day.append(items[1].rstrip())

    file.close()
    print(garbage_type)
    print(day)

    for count in range(0, len(garbage_type) - 1):
        with house_member_table.batch_writer() as batch:
            batch.put_item(
                Item={
                    'House': house_name,
                    'GarbageType': garbage_type[count],
                    'Day': day[count]
                }
            )


def scan():
    res = house_member_table.scan()
    print(res)


if __name__ == '__main__':
    main()
