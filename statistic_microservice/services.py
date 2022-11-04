from enum import Enum
from mimetypes import init
import os
import json
import boto3
from boto3.dynamodb.conditions import Key
from botocore.exceptions import ClientError
from settings import init_db
from dotenv import load_dotenv
from fastapi import status
load_dotenv()


db = init_db()


class DynamoDBFields(str, Enum):
    ITEM = "Item"
    ITEMS = "Items"
    ATTRS = "Attributes"
    ALL_NEW = "ALL_NEW"


def create_page(page_id: int, user_id: int, page_name: str):
    item = db.Table('Pages').get_item(Key={'page_id': page_id})
    if DynamoDBFields.ITEM in item:
        return "Page already exists", status.HTTP_400_BAD_REQUEST
    item = {
        'page_id': page_id,
        'user_id': user_id,
        'name': page_name,
        'likes': 0,
        'followers': 0,
        'follower_requests': 0,
    }
    try:
        db.Table('Pages').put_item(Item=item)
        return item, status.HTTP_201_CREATED
    except ClientError as e:
        return e.response["Error"]['Message'], status.HTTP_500_INTERNAL_SERVER_ERROR


def update_page(page_id: int, user_id: int, page_name: str):
    item = db.Table('Pages').get_item(Key={'page_id': page_id})
    if DynamoDBFields.ITEM not in item:
        return "Page doesn't exists", status.HTTP_400_BAD_REQUEST
    if item[DynamoDBFields.ITEM]['user_id'] != user_id:
        return "You don't have permission to performe update of the page", status.HTTP_403_FORBIDDEN
    try:
        item = db.Table('Pages').update_item(
            Key={'page_id': page_id},
            UpdateExpression="SET name :page_name",
            ExpressionAttributeValues={':page_name': page_name},
            ReturnValues=DynamoDBFields.ALL_NEW,
        )
        return item['Attributes'], status.HTTP_200_OK
    except ClientError as e:
        return e.response["Error"]['Message'], status.HTTP_500_INTERNAL_SERVER_ERROR


def delete_page(page_id: int, user_id: int):
    item = db.Table('Pages').get_item(Key={'page_id': page_id})
    if DynamoDBFields.ITEM not in item:
        return "Page doesn't exists", status.HTTP_400_BAD_REQUEST
    if item[DynamoDBFields.ITEM]['user_id'] != user_id:
        return "You don't have permission to performe deleting of the page", status.HTTP_403_FORBIDDEN
    try:
        db.Table('Pages').delete_item(Key={'page_id': page_id})
        return {}, status.HTTP_204_NO_CONTENT
    except ClientError as e:
        return e.response["Error"], status.HTTP_500_INTERNAL_SERVER_ERROR


def new_like(page_id: int):
    item = db.Table('Pages').get_item(Key={'page_id': page_id})
    if DynamoDBFields.ITEM not in item:
        return "Page doesn't exists", status.HTTP_400_BAD_REQUEST
    try:
        item = db.Table('Pages').update_item(
            Key={'page_id': page_id},
            UpdateExpression="ADD likes :inc",
            ExpressionAttributeValues={':inc': 1},
            ReturnValues=DynamoDBFields.ALL_NEW,
        )
        return item['Attributes'], status.HTTP_200_OK
    except ClientError as e:
        return e.response["Error"]['Message'], status.HTTP_500_INTERNAL_SERVER_ERROR


def undo_like(page_id: int):
    item = db.Table('Pages').get_item(Key={'page_id': page_id})
    if DynamoDBFields.ITEM not in item:
        return "Page doesn't exists", status.HTTP_400_BAD_REQUEST
    try:
        item = db.Table('Pages').update_item(
            Key={'page_id': page_id},
            UpdateExpression="ADD likes :inc",
            ConditionExpression="likes > :zero",
            ExpressionAttributeValues={
                ':inc': -1,
                ':zero': 0
            },
            ReturnValues=DynamoDBFields.ALL_NEW,
        )
        return item['Attributes'], status.HTTP_200_OK
    except ClientError as e:
        if e.response['Error']['Code'] == 'ConditionalCheckFailedException':
            return 'Amount of likes already is 0', status.HTTP_400_BAD_REQUEST
        return e.response["Error"]['Message'], status.HTTP_500_INTERNAL_SERVER_ERROR


def new_follow_request(page_id: int):
    item = db.Table('Pages').get_item(Key={'page_id': page_id})
    if DynamoDBFields.ITEM not in item:
        return "Page doesn't exists", status.HTTP_400_BAD_REQUEST
    try:
        item = db.Table('Pages').update_item(
            Key={'page_id': page_id},
            UpdateExpression="ADD follow_requests :inc",
            ExpressionAttributeValues={':inc': 1},
            ReturnValues=DynamoDBFields.ALL_NEW,
        )
        return item['Attributes'], status.HTTP_200_OK
    except ClientError as e:
        return e.response["Error"]['Message'], status.HTTP_500_INTERNAL_SERVER_ERROR


def undo_follow_request(page_id: int):
    item = db.Table('Pages').get_item(Key={'page_id': page_id})
    if DynamoDBFields.ITEM not in item:
        return "Page doesn't exists", status.HTTP_400_BAD_REQUEST
    try:
        item = db.Table('Pages').update_item(
            Key={'page_id': page_id},
            UpdateExpression="ADD follow_requests :inc",
            ConditionExpression="follow_requests > :zero",
            ExpressionAttributeValues={
                ':inc': -1,
                ':zero': 0
            },
            ReturnValues=DynamoDBFields.ALL_NEW,
        )
        return item['Attributes'], status.HTTP_200_OK
    except ClientError as e:
        if e.response['Error']['Code'] == 'ConditionalCheckFailedException':
            return 'Amount of follow requests already is 0', status.HTTP_400_BAD_REQUEST
        return e.response["Error"]['Message'], status.HTTP_500_INTERNAL_SERVER_ERROR


def new_follower(page_id: int):
    item = db.Table('Pages').get_item(Key={'page_id': page_id})
    if DynamoDBFields.ITEM not in item:
        return "Page doesn't exists", status.HTTP_400_BAD_REQUEST
    try:
        item = db.Table('Pages').update_item(
            Key={'page_id': page_id},
            UpdateExpression="ADD followers :inc",
            ExpressionAttributeValues={':inc': 1},
            ReturnValues=DynamoDBFields.ALL_NEW,
        )
        return item['Attributes'], status.HTTP_200_OK
    except ClientError as e:
        return e.response["Error"]['Message'], status.HTTP_500_INTERNAL_SERVER_ERROR


def undo_follower(page_id: int):
    item = db.Table('Pages').get_item(Key={'page_id': page_id})
    if DynamoDBFields.ITEM not in item:
        return "Page doesn't exists", status.HTTP_400_BAD_REQUEST
    try:
        item = db.Table('Pages').update_item(
            Key={'page_id': page_id},
            UpdateExpression="ADD followers :inc",
            ConditionExpression="followers > :zero",
            ExpressionAttributeValues={
                ':inc': -1,
                ':zero': 0
            },
            ReturnValues=DynamoDBFields.ALL_NEW,
        )
        return item['Attributes'], status.HTTP_200_OK
    except ClientError as e:
        if e.response['Error']['Code'] == 'ConditionalCheckFailedException':
            return 'Amount of followers already is 0', status.HTTP_400_BAD_REQUEST
        return e.response["Error"]['Message'], status.HTTP_500_INTERNAL_SERVER_ERROR


def get_statistic(page_id: int, user_id: int):
    item = db.Table('Pages').get_item(Key={'page_id': page_id})
    if DynamoDBFields.ITEM not in item:
        return "Page doesn't exists", status.HTTP_400_BAD_REQUEST
    if item[DynamoDBFields.ITEM]['user_id'] != user_id:
        return "You don't have permission to performe update of the page", status.HTTP_403_FORBIDDEN
    return item['Item'], status.HTTP_200_OK
