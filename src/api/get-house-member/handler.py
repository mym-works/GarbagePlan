# -*- coding: utf-8 -*-
import json
import boto3
from boto3.dynamodb.conditions import Key, Attr

dynamodb = boto3.resource('dynamodb')


def items_scan(house_name):
    dynamodb_table = dynamodb.Table('borderless-house-members')
    response = dynamodb_table.scan(
        FilterExpression=Key('House').eq(house_name)
    )
    return response['Items']


def main(event, context):
    event_path = event['path']
    house_name = (event_path.split('/'))[-1]

    house_member = items_scan(house_name.capitalize())

    response = {
        "statusCode": 200,
        "headers": {
            "content-type": "application/json"
        },
        "body": json.dumps(house_member, ensure_ascii=False)
    }

    return response
