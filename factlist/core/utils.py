import threading
import json
import os

import boto3
import requests
from django.core.files.temp import NamedTemporaryFile


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

        client.publish(
            TopicArn=os.environ.get("AWS_SNS_ARN") + self.sns_type,
            Message=json.dumps({"default": json.dumps(self.message)}),
            MessageStructure="json"
        )


def send_sns(message, sns_type):
    SnsThread(message, sns_type).start()


class KinesisThread(threading.Thread):
    def __init__(self, stream_name, data, partition_key):
        self.stream_name = stream_name
        self.data = data
        self.partition_key = partition_key
        threading.Thread.__init__(self)

    def run(self):
        client = boto3.client("kinesis")

        client.put_record(
            StreamName=self.stream_name,
            Data=self.data,
            PartitionKey=self.partition_key
        )


def stream_kinesis(stream_name, data, partition_key):
    KinesisThread(stream_name, data, partition_key).start()


def extract_profile_image(link):
    """
    Getting the profile image from Twitter

    First we need to modify the url taken from Twitter API. Twitter API gives profile image urls like this:
    https://pbs.twimg.com/profile_images/751530273670594560/CbL6FI1l_normal.jpg
    This url contains a thumbnail of the original image. Original image url is almost same but without the "_normal"
    part in the thumbnail url. So we need a url like this:
    https://pbs.twimg.com/profile_images/751530273670594560/CbL6FI1l.jpg

    Three lines below splits the url by "." and cuts the "com/profile_images/751530273670594560/CbL6FI1l_normal"
    part by the last seven character. It becomes: "com/profile_images/751530273670594560/CbL6FI1l".
    """
    if link == "https://abs.twimg.com/sticky/default_profile_images/default_profile_normal.png":
        # User doesn't have a profile image on Twitter.
        return None, None
    url = link.split(".")
    extension = "." + url[-1]
    url[-2] = url[-2][:-7]
    url = ".".join(url)

    # Downloading the image from Twitter
    request = requests.get(url, stream=True)
    image = NamedTemporaryFile()
    for block in request.iter_content(1024 * 8):
        if not block:
            break
        image.write(block)
    return image, extension
