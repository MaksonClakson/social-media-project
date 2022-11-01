import boto3
from botocore.exceptions import ClientError
import os
from rest_framework import status
from datetime import datetime

AWS_CREDENTIALS = {
    "AWS_ACCESS_KEY_ID": os.getenv("AWS_ACCESS_KEY_ID"),
    "AWS_SECRET_ACCESS_KEY": os.getenv("AWS_SECRET_ACCESS_KEY"),
    "AWS_URL": f"http://{os.getenv('AWS_HOST')}:{os.getenv('AWS_PORT')}",
    "AWS_SES_REGION_NAME": os.getenv("AWS_DEFAULT_REGION"),
}

s3_resource = boto3.resource(
    's3',
    endpoint_url=AWS_CREDENTIALS["AWS_URL"],
    region_name=AWS_CREDENTIALS["AWS_SES_REGION_NAME"],
    aws_access_key_id=AWS_CREDENTIALS["AWS_ACCESS_KEY_ID"],
    aws_secret_access_key=AWS_CREDENTIALS["AWS_SECRET_ACCESS_KEY"]
)


def create_bucket():
    """
    Creates a S3 bucket.
    """
    try:
        response = s3_resource.create_bucket(
            Bucket=os.getenv("AWS_BUCKET_NAME"),
            CreateBucketConfiguration={'LocationConstraint': AWS_CREDENTIALS["AWS_SES_REGION_NAME"]}
        )
        print(response)
    except ClientError as e:
        return e.response["Error"]['Message'], status.HTTP_500_INTERNAL_SERVER_ERROR
    else:
        return response


def upload_image(file, user_pk):
    """
    Upload an image to a S3 bucket.
    """
    try:
        print("file attr ---------" + str(file.__dict__))
        ALLOWED_EXTENSIONS = ['png', 'jpg', 'jpeg']
        if not any(ext in format(file.content_type) for ext in ALLOWED_EXTENSIONS):
            return "Format is not allowed", status.HTTP_400_BAD_REQUEST
        s3_key = f"({datetime.now().timestamp()})_{user_pk}_{file.name}"
        print("s3_key ----" + str(s3_key))
        # response = s3_resource.upload_fileobj(
        #     Fileobj=file,
        #     Bucket=os.getenv("AWS_BUCKET_NAME"),
        #     Key=s3_key
        # )
        object = s3_resource.Object(os.getenv("AWS_BUCKET_NAME"), s3_key)
        result = object.put(Body=file)
        print("repose" + str(result.__dict__))
    except ClientError as e:
        return e.response["Error"]['Message'], status.HTTP_500_INTERNAL_SERVER_ERROR
    if result['ResponseMetadata']['HTTPStatusCode'] == 200:
        return 'File Uploaded Successfully', status.HTTP_200_OK
    else:
        return 'File Not Uploaded', status.HTTP_500_INTERNAL_SERVER_ERROR


def download_file(file_name, bucket, object_name=None):
    """
    Download a file to a S3 bucket.
    """
    try:
        response = s3_resource.Bucket(bucket).download_file(
            object_name, file_name)
    except ClientError as e:
        return e.response["Error"]['Message'], status.HTTP_500_INTERNAL_SERVER_ERROR
    else:
        return response


def main():
    """
    Main invocation function.
    """
    bucket_name = "images-on-cloud-localstack-bucket"
    s3 = create_bucket(bucket_name)


def list_buckets():
    try:
        response = s3_resource.buckets.all()
    except ClientError as e:
        return e.response["Error"]['Message'], status.HTTP_500_INTERNAL_SERVER_ERROR
    else:
        return response
