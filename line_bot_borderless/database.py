import boto3
import json
from boto3.dynamodb.conditions import Key, Attr
import logging

dynamodb = boto3.resource('dynamodb')
house_member_table = dynamodb.Table('borderless-house')


def member_read():
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)

    res = house_member_table.query(
        KeyConditionExpression=Key('house').eq("oimachi")
    )
    for row in res['Items']:
        logger.info(row)
