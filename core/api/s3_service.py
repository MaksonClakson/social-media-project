import boto3
from botocore.exceptions import ClientError
import os
from rest_framework import status
from datetime import datetime
from api.aws import s3_client


def upload_image(file, user_pk):
    """
    Upload an image to a S3 bucket.
    """
    try:
        ALLOWED_EXTENSIONS = ['png', 'jpg', 'jpeg']
        if not any(ext in format(file.content_type) for ext in ALLOWED_EXTENSIONS):
            return "Format is not allowed", status.HTTP_400_BAD_REQUEST
        s3_key = f"{datetime.now().timestamp()}_{user_pk}_{file.name}"
        result = s3_client.put_object(
            Body=file, 
            Bucket=os.getenv("AWS_BUCKET_NAME"),
            Key=s3_key
        )
    except ClientError as e:
        return e.response["Error"]['Message'], status.HTTP_500_INTERNAL_SERVER_ERROR
    if result['ResponseMetadata']['HTTPStatusCode'] == 200:
        return result['ResponseMetadata']['HTTPHeaders']['location'] + '/' + s3_key, status.HTTP_200_OK
    else:
        return 'File Not Uploaded', status.HTTP_500_INTERNAL_SERVER_ERROR
