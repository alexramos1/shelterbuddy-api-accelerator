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
import os

db = Database()
conn = ShelterBuddyConnection()
s3client = boto3.client('s3')
bucket = os.environ['AWS_S3_BUCKET']

dynamodb = boto3.resource('dynamodb', region_name='us-west-1')
syncTable = dynamodb.Table('sb-sync')
detailTable = dynamodb.Table('sb-animal-details')

def preparePhotos(animal):
    photos = conn.fetchPhotoLinks(animal['Id'])
    print(photos)
    for photo in photos:
        sizes = [ 1024, 640, 480, 320, 240 ]
        if('PhotoThumbnailFormat' in photo):
            photoFormat = photo['PhotoThumbnailFormat'].replace("<size>", "%d")
        else:
            photoFormat = photo['Photo'].replace('-jpg/1024---n', '-jpg/%d---n')

        del photo['Photo']
        del photo['PhotoThumbnailFormat']
        photo['Versions'] = []  

        for thSize in sizes:
            photoPath = photoFormat % thSize
            s3path = photoPath[1:]
            photoPayload = conn.fetchPhotoPayload(photoPath)
            s3client.put_object(ContentType='image/jpeg', Bucket=bucket, Key=s3path, Body=photoPayload)
            photo['Versions'].append({ str(thSize): photoPath })
            
    animal['Photos'] = photos
    
def action(animals):
    for animal in animals:
        conn.resolve(animal, 'Uri', lambda uri: conn.fetchUri(uri))
        triageKeep = localrules.triageForWeb(animal)

        if(triageKeep):
            # inline and prefetch the photo urls
            preparePhotos(animal)
            # saves the summarized animal for searching
            db.save(animal)
            # save the full original animal details
            detailTable.put_item(Item={'Id': animal['Id'], 'rawData': json.dumps(animal, cls=DecimalEncoder) })
        else:
            db.delete(animal)
            try:
                detailTable.delete_item(Key={'Id': animal['Id']})
            except:
                'ignore'
            
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