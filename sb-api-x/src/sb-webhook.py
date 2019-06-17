# implement a generic web-hook: any request received is written to S3

import boto3
import json
import datetime
import uuid
import os

s3client = boto3.client('s3')
bucket = os.environ['AWS_S3_BUCKET']

def lambda_handler(event, context):
    now = datetime.datetime.now()
    s3path = "%04d-%02d/%02d/%02d:%02d:%02d.%s" % (now.year, now.month, now.day, now.hour, now.minute, now.second, uuid.uuid4()) 
    s3client.put_object(Bucket=bucket, Key=s3path, Body=json.dumps(event))
    return {
        'statusCode': 200,
        'headers': { },
        'body': "ok"
    }
