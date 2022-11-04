import os
import boto3
from boto3.resources.base import ServiceResource
from dotenv import load_dotenv
load_dotenv()

IS_PRODUCTION = os.getenv("DEBUG", "False") == "False"

AWS_CREDENTIALS = {
    "AWS_ACCESS_KEY_ID": os.getenv("AWS_ACCESS_KEY_ID"),
    "AWS_SECRET_ACCESS_KEY": os.getenv("AWS_SECRET_ACCESS_KEY"),
    "AWS_URL": f"http://{os.getenv('AWS_HOST')}:{os.getenv('AWS_PORT')}",
    "AWS_SES_REGION_NAME": os.getenv("AWS_DEFAULT_REGION"),
}


def init_db() -> ServiceResource:
    # create database
    db = boto3.resource(
        'dynamodb',
        endpoint_url=AWS_CREDENTIALS["AWS_URL"],
        region_name=AWS_CREDENTIALS["AWS_SES_REGION_NAME"],
        aws_access_key_id=AWS_CREDENTIALS["AWS_ACCESS_KEY_ID"],
        aws_secret_access_key=AWS_CREDENTIALS["AWS_SECRET_ACCESS_KEY"]
    )
    # create Pages table in development mode
    if len(list(db.tables.all())) < 1 and not IS_PRODUCTION:
        table = db.create_table(
            TableName='Pages',
            KeySchema=[
                {
                    'AttributeName': 'page_id',
                    'KeyType': 'HASH'
                }
            ],
            AttributeDefinitions=[
                {
                    'AttributeName': 'page_id',
                    'AttributeType': 'N'
                },
                {
                    'AttributeName': 'user_id',
                    'AttributeType': 'N'
                }
            ],
            ProvisionedThroughput={
                'ReadCapacityUnits': 5,
                'WriteCapacityUnits': 5
            },
            GlobalSecondaryIndexes=[
                {
                    'IndexName': 'user_id_index',
                    'KeySchema': [
                        {
                            'AttributeName': 'user_id',
                            'KeyType': 'HASH'
                        }
                    ],
                    'ProvisionedThroughput': {
                        'ReadCapacityUnits': 5,
                        'WriteCapacityUnits': 5
                    },
                    # attributes wich will be copied to GSI table
                    'Projection': {
                        "ProjectionType": "ALL"
                    }
                }
            ]
        )
        print(table)
    return db


def drop_table_pages(db):
    table = db.Table('Pages')
    table.delete()
