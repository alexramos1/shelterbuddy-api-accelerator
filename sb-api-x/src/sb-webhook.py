# implement a generic web-hook: any request received is written to SQS
import boto3
import json
import os
import uuid
from datetime import datetime

client = boto3.client('sqs')
queue  = os.environ['SQS_WEBHOOK']

s3bucket = 'sb-webhook'
s3client = boto3.client('s3')

def lambda_handler(event, context):

    log = client.send_message(QueueUrl=queue, MessageBody=json.dumps(event))
    print (log)
    
    sequentialPath = datetime.now().strftime('%Y/%m/%d/%H.%M.%S.%f.') + uuid.uuid4().hex + '.json'
    log = s3client.put_object(Bucket=s3bucket, Key=sequentialPath, Body=json.dumps(event).encode('utf-8', 'replace'))
    print(log)
    
    return {
        'statusCode': 200,
        'headers': { },
        'body': "ok"
    }
