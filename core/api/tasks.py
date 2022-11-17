import os
from api.aws import ses_client
from celery import shared_task


def verify_emails():
    response = ses_client.verify_email_identity(
        EmailAddress = os.getenv("AWS_VERIFIED_EMAIL")
    )
    return response


@shared_task
def notify_follower_about_new_post(page_name, post_content, email):
    """
    Celery Task that send email through SES
    """
    response = ses_client.send_email(
        Destination={
            "ToAddresses": [email],
        },
        Message={
            "Body": {
                "Text": {
                    "Charset": "UTF-8",
                    "Data": post_content,
                }
            },
            "Subject": {
                "Charset": "UTF-8",
                "Data": "New post on " + str(page_name) + " page!",
            },
        },
        Source=os.getenv("AWS_VERIFIED_EMAIL"),
    )
    return response
