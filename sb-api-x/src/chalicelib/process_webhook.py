# implement a generic web-hook: any request received is written to S3
import boto3
import json
import os
from .database import Database

client = boto3.client('sqs')
queue  = os.environ['SQS_WEBHOOK']
db = Database()

def parse(jsonStr):
    event = json.loads(jsonStr)
    body = json.loads(event['body'])
    if body['DeletedDateUtc']:
        return (body['DeletedDateUtc'], body['AnimalId'])
    else:
        raise Exception('missing DeletedDateUtc')
  
def processWebhooks(cutoffTimestamp):
    while True:
        msg = client.receive_message(QueueUrl=queue)
        if not('Messages' in msg):
            print("No Messages")
            return 
        for msg1 in msg['Messages']:
            (deletedDt, animalId) = parse(msg1['Body'])
            print("received from sqs-webhook: %s @ %s" % (animalId, deletedDt))
            if deletedDt < cutoffTimestamp:
                print('DELETED BY WEBHOOK: %d' %(animalId))
                db.delete({'Id': animalId })
                client.delete_message(QueueUrl=queue, ReceiptHandle=msg1['ReceiptHandle'])
            else:
                # avoid a race condition where deletion could occur before a record is created, resulting in an orphaned record
                print("SKIP due to deletedDt >= cutoffTimestamp : %s >= %s (try again later when cutoffTimestamp has increased)" % (deletedDt, cutoffTimestamp))
                return
   
if __name__ == '__main__':
    import sys
    processWebhooks(sys.argv[1])
