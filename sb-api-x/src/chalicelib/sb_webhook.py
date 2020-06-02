# implement a generic web-hook: any request received is written to SQS
import boto3
import json
import os
import uuid
from datetime import datetime
from .database import Database, byline
from chalicelib.shelterbuddy import ShelterBuddyConnection, DecimalEncoder
from . import localrules

client = boto3.client('sqs')
webhookQueue  = os.environ['SQS_PREFIX'] + 'webhookQueue'
incomingQueue  = os.environ['SQS_PREFIX'] + 'incomingQueue'
db = Database()

s3bucket = os.environ['S3_WEBHOOK_BUCKET']
s3client = boto3.client('s3')
conn = ShelterBuddyConnection()

def intake(event):

    log = client.send_message(QueueUrl=webhookQueue, MessageBody=json.dumps(event, cls=DecimalEncoder))
    print (log)
    
    sequentialPath = datetime.now().strftime('%Y/%m/%d/%H.%M.%S.%f.') + uuid.uuid4().hex + '.json'
    log = s3client.put_object(Bucket=s3bucket, Key=sequentialPath, Body=json.dumps(event, cls=DecimalEncoder).encode('utf-8', 'replace'))
    print(log)
    
    return "ok"

def processWebhooks():
    while True:
        msg = client.receive_message(QueueUrl=webhookQueue)
        if not('Messages' in msg):
            print("No Messages in Queue")
            return 
        for msg1 in msg['Messages']:
            event = json.loads(msg1['Body'])
            body = json.loads(event['body'])

            deletedDateUtc = None
            refreshId = None

            if 'DeletedDateUtc' in body:
                (deletedDateUtc, deletedAnimalId) = (body['DeletedDateUtc'], body['AnimalId'])
                print("webhook DELETE: %s @ %s" % (deletedAnimalId, deletedDateUtc))

            if 'MergeDateUtc' in body:
                (deletedDateUtc, deletedAnimalId, keptId) = (body['MergeDateUtc'], body['DeletedRecord'], body['KeptRecord']['Id'])
                print("webhook MERGE: %s -> %s @ %s" % (deletedAnimalId, keptId, deletedDateUtc))
                refreshId = keptId

            if deletedDateUtc is not None:
                db.delete({'Id': deletedAnimalId })

            elif 'Photos' in body:
                print("webhook PHOTOS: %s @ %s" % (body['Id'], len(body['Photos'])))
                refreshId = body['Id']

            elif 'Id' in body:
                print("webhook UPDATE: %s" % byline(body))
                refreshId = body['Id']
                
            else:
                print('webhook UNKNOWN: ' + json.dumps(body, cls=DecimalEncoder))
                
            if refreshId:
                freshData = conn.fetchAnimal(refreshId)
                print('fetched: %s' % byline(freshData))
                if localrules.triageForWeb(freshData):
                    response = client.send_message(QueueUrl=incomingQueue, MessageBody=json.dumps(freshData, cls=DecimalEncoder))
                    print('sent: MessageId=%s, BodyMD5=%s' % (response['MessageId'], response['MD5OfMessageBody']))
                else:
                    db.delete(freshData)

            response = client.delete_message(QueueUrl=webhookQueue, ReceiptHandle=msg1['ReceiptHandle'])
            print('delete response = ' + str(response))
