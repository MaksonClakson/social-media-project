import os
from api.aws import ses_client


def notify_follower_about_new_post(page_name, post_content, email):
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
                "Data": "New post on " + page_name + " page!",
            },
        },
        Source=os.getenv("AWS_VERIFIED_EMAIL"),
    )
    return response
