import boto3
import json
from boto3.dynamodb.conditions import Key, Attr
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)

dynamodb = boto3.resource('dynamodb')


def items_scan(table_name):
    dynamodb_table = dynamodb.Table(table_name)
    response = dynamodb_table.scan()
    return response['Items']


def items_read(table_name, house_name):
    dynamodb_table = dynamodb.Table(table_name)
    response = dynamodb_table.query(
        KeyConditionExpression=Key('House').eq(house_name)
    )
    return response["Items"]


def items_update(table_name, house_name, new_people_in_charge_queue):
    dynamodb_table = dynamodb.Table(table_name)
    response = dynamodb_table.update_item(
        Key={
            'House': house_name
        },
        UpdateExpression='set Room = :r',
        ExpressionAttributeValues={
            ':r': new_people_in_charge_queue
        },
        ReturnValues='UPDATED_NEW'
    )
    logger.info(response)
