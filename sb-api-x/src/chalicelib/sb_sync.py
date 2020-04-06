#
# An AWS Lambda function to periodically pre-load Shelterbuddy API data into a DynamoDB syncTable.
#
from .shelterbuddy import ShelterBuddyConnection
from .database import Database, byline
from . import localrules
from datetime import datetime, timedelta
import boto3
from boto3.dynamodb.conditions import Key
import json
import os
from .sb_webhook import processWebhooks

db = Database()
conn = ShelterBuddyConnection()
s3client = boto3.client('s3')
sqs = boto3.client('sqs')
incomingQueue = os.environ['SQS_PREFIX'] + 'incomingQueue'

dynamodb = boto3.resource('dynamodb')
syncTable = dynamodb.Table('sb-sync')

def action(animals):
    for animal in animals:
        triageKeep = localrules.triageForWeb(animal)

        if(triageKeep):
            sqs.send_message(QueueUrl=incomingQueue, MessageBody=json.dumps(animal, default=str))
            print('QUEUED: ' + byline(animal))
        else:
            db.delete(animal)

def persist(target, cutoff, nextCut):
    if target:
        info = target + '#' + cutoff + '#' + nextCut
    else:
        info = '#' + nextCut + '#'
    syncTable.put_item(Item={ 'hashKey': 'continuation', 'info':  info})

def sync():
    
    info = syncTable.query(KeyConditionExpression=Key('hashKey').eq('continuation'))
    (target,cutoff,nextCut) = (None,None,None)
    
    if(info['Items']):
        (target,cutoff,nextCut) = info['Items'][0]['info'].split('#')
    
    if(target is None or target == ''):
        target = "/api/v2/animal/list?PageSize=1000"
    
    if(cutoff is None or cutoff == ''):
        # initial load, database is empty
        days = int(os.environ['INITIAL_LOAD_DAYS'])
        cutoff = (datetime.today() - timedelta(days=days)).replace(microsecond=0).isoformat() + "Z"
        
    if(nextCut == ''):
        nextCut = None
    
    print("target = %s, cutoff = %s, nextCut = %s" % (target, cutoff, nextCut))
    
    conn.loadAnimals(target, cutoff, nextCut, action, persist)
    processWebhooks(cutoff)
