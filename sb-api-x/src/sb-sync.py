#
# An AWS Lambda function to periodically pre-load Shelterbuddy API data into a DynamoDB syncTable.
#
from shelterbuddy import ShelterBuddyConnection, DecimalEncoder
from database import Database
from datetime import datetime, timedelta
import localrules
import boto3
from boto3.dynamodb.conditions import Key
import json

db = Database()
conn = ShelterBuddyConnection()

dynamodb = boto3.resource('dynamodb', region_name='us-west-1')
syncTable = dynamodb.Table('sb-sync')
detailTable = dynamodb.Table('sb-animal-details')

def action(animals):
    for animal in animals:
        conn.resolve(animal, 'Uri', lambda uri: conn.fetchUri(uri))

        triageKeep = localrules.triageForWeb(animal)

        if(triageKeep):
            # inline the photo urls
            animal['Photos'] = conn.fetchPhotos(animal['Id'])
            # saves the summarized animal for searching
            db.save(animal)
            # save the full original animal details
            detailTable.put_item(Item={'Id': animal['Id'], 'rawData': json.dumps(animal, cls=DecimalEncoder) })
        else:
            db.delete(animal)
            detailTable.delete_item(Key={'Id': animal['Id']})
            
    print('Processed: ' + str([animal['Id'] for animal in animals]))

def persist(target, last, cutoff):
    info = (target + '#' + cutoff) if target else '#' + last
    syncTable.put_item(Item={ 'hashKey': 'continuation', 'info':  info})

def lambda_handler(event, context):
    
    info = syncTable.query(KeyConditionExpression=Key('hashKey').eq('continuation'))
    (target,cutoff) = (None,None)
    
    if(info['Items']):
        (target,cutoff) = info['Items'][0]['info'].split('#')
    
    if(target is None or target == ''):
        target = "/api/v2/animal/list?PageSize=100"
    
    if(cutoff is None):
        cutoff = (datetime.today() - timedelta(days=localrules.days)).replace(microsecond=0).isoformat() + "Z"
    
    print("target = " + target)
    print("cutoff = " + cutoff)
    
    conn.loadAnimals(target, cutoff, action, persist)

if __name__ == "__main__":
    lambda_handler(None,None)