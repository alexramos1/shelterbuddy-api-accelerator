# implement a generic web-hook: any request received is written to SQS
import boto3
import json
import os

client = boto3.client('sqs')
queue  = os.environ['SQS_WEBHOOK']

def lambda_handler(event, context):
    client.send_message(QueueUrl=queue, MessageBody=json.dumps(event))
    return {
        'statusCode': 200,
        'headers': { },
        'body': "ok"
    }
