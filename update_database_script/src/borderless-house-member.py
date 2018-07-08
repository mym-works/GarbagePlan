import boto3
from boto3 import dynamodb
from boto3.session import Session
from boto3.dynamodb.conditions import Key, Attr

dynamodb_session = Session(profile_name="mayama-cli",
                           region_name="ap-northeast-1")
dynamodb = dynamodb_session.resource('dynamodb')
house_member_table = dynamodb.Table("oimachi-house-members")


def main():
    update()
    confirm()


def update():
    file = open("../conf/borderless-house-member.csv", "r")
    groupIds = []
    rooms = []
    names = []
    for line in file:
        items = line.split(",")
        groupIds.append(items[0])
        rooms.append(items[1])
        names.append(items[3])
    file.close()

    with house_member_table.batch_writer() as batch:
        for count in range(20):
            rooms[count]
            batch.put_item(
                Item={
                    'Room': rooms[count],
                    'Name': names[count],
                    'GroupId': groupIds[count]
                }
            )


def confirm():
    res = house_member_table.query(
        KeyConditionExpression=Key('Room').eq("1A")
    )
    for row in res['Items']:
        print(row)


if __name__ == '__main__':
    main()
