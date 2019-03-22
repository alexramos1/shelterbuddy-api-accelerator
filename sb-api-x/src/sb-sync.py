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

dynamodb = boto3.resource('dynamodb', region_name='us-west-1')
table = dynamodb.Table('sb-sync')

def action(animals):    
    localrules.applyFilters(conn,animals, db.save, db.delete)

def persist(target, last, cutoff):
    info = (target + '#' + cutoff) if target else '#' + last
    table.put_item(Item={ 'hashKey': 'continuation', 'info':  info})

def lambda_handler(event, context):
    
    info = table.query(KeyConditionExpression=Key('hashKey').eq('continuation'))
    (target,cutoff) = (None,None)
    
    if(info['Items']):
        (target,cutoff) = info['Items'][0]['info'].split('#')
    
    if(target is None or target == ''):
        target = "/api/v2/animal/list?PageSize=100"   
    
    if(cutoff is None):
        cutoff = (datetime.today() - timedelta(days=localrules.days)).replace(microsecond=0).isoformat() + "Z"
    
    print("target = " + target)
    print("cutoff = " + cutoff)
    
    for animal in conn._loadAnimals(target, cutoff, action, persist):
        print(animal['Id'])

if __name__ == "__main__":
    lambda_handler(None,None)