import boto3
import os

AWS_CREDENTIALS = {
    "AWS_ACCESS_KEY_ID": os.getenv("AWS_ACCESS_KEY_ID"),
    "AWS_SECRET_ACCESS_KEY": os.getenv("AWS_SECRET_ACCESS_KEY"),
    "AWS_URL": f"http://{os.getenv('AWS_HOST')}:{os.getenv('AWS_PORT')}",
    "AWS_SES_REGION_NAME": os.getenv("AWS_DEFAULT_REGION"),
}

s3_client = boto3.client(
    's3',
    endpoint_url=AWS_CREDENTIALS["AWS_URL"],
    region_name=AWS_CREDENTIALS["AWS_SES_REGION_NAME"],
    aws_access_key_id=AWS_CREDENTIALS["AWS_ACCESS_KEY_ID"],
    aws_secret_access_key=AWS_CREDENTIALS["AWS_SECRET_ACCESS_KEY"]
)

if not [bucket for bucket in s3_client.list_buckets()['Buckets'] if bucket['Name'] == os.getenv("AWS_BUCKET_NAME")]:
    s3_client.create_bucket(
        Bucket=os.getenv("AWS_BUCKET_NAME"),
        CreateBucketConfiguration={
            'LocationConstraint': AWS_CREDENTIALS["AWS_SES_REGION_NAME"]}
    )

ses_client = boto3.client(
    'ses',
    endpoint_url=AWS_CREDENTIALS["AWS_URL"],
    region_name=AWS_CREDENTIALS["AWS_SES_REGION_NAME"],
    aws_access_key_id=AWS_CREDENTIALS["AWS_ACCESS_KEY_ID"],
    aws_secret_access_key=AWS_CREDENTIALS["AWS_SECRET_ACCESS_KEY"]
)