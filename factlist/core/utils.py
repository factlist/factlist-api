import threading
import json
import os

import boto3


class SnsThread(threading.Thread):
    def __init__(self, message, sns_type):
        self.message = message
        self.sns_type = sns_type
        threading.Thread.__init__(self)

    def run(self):
        client = boto3.client(
            "sns",
            region_name="us-east-1",
            aws_access_key_id=os.environ.get("AWS_ACCESS_KEY_ID"),
            aws_secret_access_key=os.environ.get("AWS_SECRET_ACCESS_KEY"),
        )

        response = client.publish(
            TopicArn=os.environ.get("AWS_SNS_ARN") + self.sns_type,
            Message=json.dumps({"default": json.dumps(self.message)}),
            MessageStructure="json"
        )


def send_sns(message, sns_type):
    SnsThread(message, sns_type).start()
