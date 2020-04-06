import boto3
import os
from chalicelib.sb_webhook import processWebhooks
import datetime 

s3 = boto3.resource('s3')
bucket = s3.Bucket('sb-webhook')
sqs = boto3.client('sqs')

for obj in bucket.objects.filter(Prefix='2020/04/04/'):
    print(obj.key)
    body = obj.get()['Body'].read()
    sqs.send_message(QueueUrl=os.environ['SQS_PREFIX'] + 'webhookQueue', MessageBody=body.decode('utf-8'))
    
    processWebhooks('2020-04-05 00:00:00')