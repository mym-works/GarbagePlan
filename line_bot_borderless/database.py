import boto3
import json
from boto3.dynamodb.conditions import Key, Attr
import logging

dynamodb = boto3.resource('dynamodb')
house_member_table = dynamodb.Table('borderless-house-members')
this_week_garbage_charge_table = dynamodb.Table(
    'borderles-this-week-garbage-charge')


def member_read():
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)

    res = house_member_table.query(
        KeyConditionExpression=Key('House').eq("Oimachi")
    )
    return res


def this_week_charger():
    res = this_week_garbage_charge_table.query(
        KeyConditionExpression=Key('House').eq("Oimachi")
    )
    return res
