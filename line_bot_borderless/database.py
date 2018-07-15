import boto3
import json
from boto3.dynamodb.conditions import Key, Attr
import logging

dynamodb = boto3.resource('dynamodb')


def items_read(table_name):
    dynamodb_table = dynamodb.Table(table_name)
    response = dynamodb_table.query(
        KeyConditionExpression=Key('House').eq("Oimachi")
    )
    return response["Items"]
