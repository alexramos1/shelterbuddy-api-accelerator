#
# An AWS Lambda function to periodically pre-load Shelterbuddy API data into a DynamoDB table.
#
from shelterbuddy import ShelterBuddyConnection
from database import Database
from datetime import datetime, timedelta
import localrules
import boto3
from boto3.dynamodb.conditions import Key

db = Database()
conn = ShelterBuddyConnection()

# using Dynamodb to store continuation information (next timestamp)
dynamodb = boto3.resource('dynamodb', region_name='us-west-1')
table = dynamodb.Table('sdhs_sync')
info = table.query(KeyConditionExpression=Key('hashKey').eq('continuation'))

if(info['Items']):
    print(info)
    (target,cutoff) = info['Items'][0]['info'].split('#')
else:
    target = "/api/v2/animal/list?PageSize=200"
    cutoff = (datetime.today() - timedelta(days=localrules.days)).replace(microsecond=0).isoformat() + "Z"
    
action = lambda animals: localrules.applyFilters(conn,animals, db.save, db.delete)
persist = lambda target: table.put_item(Item={ 'hashKey': 'continuation', 'info':  (target + '#' + cutoff) if target else None})

for animal in conn._loadAnimals(target, cutoff, action, persist):
    print(animal['Id'])
