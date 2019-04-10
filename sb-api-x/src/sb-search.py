import json
import boto3
import traceback
from database import Database
from database import opt

db = Database()
dynamodb = boto3.client('dynamodb', region_name = 'us-west-1')

#Example Query:
#{
#    "AnimalType": [
#        "Cat"
#    ],
#    "Location": [
#        "Oceanside Campus - Dogs"
#    ],
#    "StatusCategory": [
#        "available"
#    ]
#}
def query(StatusCategory, AnimalType, Location):
    if len(StatusCategory) != 1:
        return { 'error': 'StatusCategory parameter must be exactly 1 value.' }
    if len(AnimalType) < 1:
        return { 'error': 'AnimalType parameter must be at least 1 value or ALL.' }
    if len(Location) < 1:
        return { 'error': 'Location parameter must be at least 1 value or ALL.' }
    
    if AnimalType == ['ALL'] and Location == ['ALL']:
        # query using only the StatusCategory
        response = dynamodb.query(
            TableName=db.tableName,
            IndexName='StatusCategory-LocationKey-index',
            Select='ALL_ATTRIBUTES',
            ConsistentRead=False,
            KeyConditionExpression='StatusCategory = :sc',
            ExpressionAttributeValues={
                ':sc': { 'S': StatusCategory[0] }
            }
        )['Items']
    elif AnimalType == ['ALL']:
        # query using only the StatusCategory and Location
        response = []
        for eachLocation in Location:
            resp = dynamodb.query(
                TableName=db.tableName,
                IndexName='StatusCategory-LocationKey-index',
                Select='ALL_ATTRIBUTES',
                ConsistentRead=False,
                KeyConditionExpression='StatusCategory = :sc AND LocationKey = :loc',
                ExpressionAttributeValues={
                    ':sc': { 'S': StatusCategory[0] },
                    ':loc': { 'S': eachLocation },
                }
            )
            response.extend(resp['Items'])
    elif Location == ['ALL']:
        # query using only the StatusCategory and AnimalType
        response = []
        for eachAnimalType in AnimalType:
            resp = dynamodb.query(
                TableName=db.tableName,
                IndexName='StatusCategory-AnimalType-index',
                Select='ALL_ATTRIBUTES',
                ConsistentRead=False,
                KeyConditionExpression='StatusCategory = :sc AND AnimalType = :animalType',
                ExpressionAttributeValues={
                    ':sc': { 'S': StatusCategory[0] },
                    ':animalType': { 'S': eachAnimalType },
                }
            )
            response.extend(resp['Items'])
    else:
        # query using the StatusCategory and AnimalType, with a filter on Location
        response = []
        for eachAnimalType in AnimalType:
            eav = { ':sc': { 'S': StatusCategory[0] },
                    ':animalType': { 'S': eachAnimalType }
            }
            for i in range(0, len(Location)):
                eav[':loc' + str(i+1)] = { 'S' : Location[i] }
            locRefs = ','.join([':loc' + str(i+1) for i in range(0,len(Location))])
            response.extend(dynamodb.query(
                TableName=db.tableName,
                IndexName='StatusCategory-AnimalType-index',
                Select='ALL_ATTRIBUTES',
                ConsistentRead=False,
                KeyConditionExpression='StatusCategory = :sc AND AnimalType = :animalType',
                ExpressionAttributeValues=eav,
                FilterExpression='LocationKey IN (%s)' % locRefs
            )['Items'])
    #
    # convert from dynamodb storage format while removing unused fields
    #
    return [{
       "AnimalId": int(js['Id']['N']),
       "AnimalType": opt(js, lambda js: js['AnimalType']['S']),
       "Location": opt(js, lambda js: js['LocationKey']['S']),
       "Status": opt(js, lambda js: js['Status']['S']),
       "Name": opt(js, lambda js: js['Name']['S'].strip(), 'Unknown'),
       "Sex": opt(js, lambda js: js['Sex']['S'], 'Unknown'),
       "Breed": {
            "Primary": opt(js, lambda js: js['Breed']['M']['Primary']['S']),
            "Secondary": opt(js, lambda js: js['Breed']['M']['Secondary']['S']),
            "IsCrossBreed": opt(js, lambda js: js['Breed']['M']['IsCrossBreed']['BOOL'])
       },
       "Age": {
            "Years": opt(js, lambda js: int(js['Age']['M']['Years']['N'])),
            "Months": opt(js, lambda js: int(js['Age']['M']['Months']['N'])),
            "Weeks": opt(js, lambda js: int(js['Age']['M']['Weeks']['N'])),
            "IsApproximate": opt(js, lambda js: js['Age']['M']['IsApproximate']['BOOL']),
            "AgeGroup": opt(js, lambda js: js['Age']['M']['AgeGroup']['S'])
       },
       "MainPhoto": opt(js, lambda js: {
              #"Versions": [list(m['M'].keys())[0] for m in js['MainPhoto']['M']['Versions']['L']],
              "default": js['MainPhoto']['M']['Versions']['L'][3]['M']['320']['S']
       }) 
    } for js in response]

def lambda_handler(event, context):
    try:
        mq = event['multiValueQueryStringParameters']
        response = query(mq['StatusCategory'], mq['AnimalType'], mq['Location'])
        return {
            'statusCode': 200,
            'headers': { 'Access-Control-Allow-Origin': '*' },
            'body': json.dumps({'request':mq, 'response':response})
        }
    except Exception as e:
        return {
            'statusCode': 200,
            'headers': { 'Access-Control-Allow-Origin': '*' },
            'body':json.dumps({'error': traceback.format_exc()})
        }
