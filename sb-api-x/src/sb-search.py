import json
import boto3
import traceback

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
            TableName='sdhs_animals',
            IndexName='StatusCategory-LocationKey-index',
            Select='ALL_ATTRIBUTES',
            ConsistentRead=False,
            KeyConditionExpression='StatusCategory = :sc',
            ExpressionAttributeValues={
                ':sc': { 'S': StatusCategory }
            }
        )
    elif AnimalType == ['ALL']:
        # query using only the StatusCategory and Location
        response = dynamodb.query(
            TableName='sdhs_animals',
            IndexName='StatusCategory-LocationKey-index',
            Select='ALL_ATTRIBUTES',
            ConsistentRead=False,
            KeyConditionExpression='StatusCategory = :sc AND LocationKey = :loc',
            ExpressionAttributeValues={
                ':sc': { 'S': StatusCategory[0] },
                ':loc': { 'S': Location[0] },
            }
        )
        #response = dynamodb.batch_get_item(
        #    RequestItems={
        #        'sdhs.animals': {
        #            'Keys': [ { 'StatusCategory':  {'S':StatusCategory[0]}, 'Location': {'S':x} } for x in Location ]
        #        }
        #    }
        #)
    #
    # convert from dynamodb storage format while removing unused fields
    #
    return [{
       "AnimalId": js['Id']['N'],
       "Name": opt(js, lambda js: js['Name']['S']),
       "Sex": js['Sex']['M']['Name']['S'],
       "Breed": {
            "Primary": js['Breed']['M']['Primary']['M']['Name']['S'],
            "Secondary": opt(js, lambda js: js['Breed']['M']['Secondary']['M']['Name']['S']),
            "IsCrossBreed": js['Breed']['M']['IsCrossBreed']['BOOL']
       },
       "Age": {
            "Years": opt(js, lambda js: js['Age']['M']['Years']['N']),
            "Months": opt(js, lambda js: js['Age']['M']['Months']['N']),
            "Weeks": opt(js, lambda js: js['Age']['M']['Weeks']['N']),
            "IsApproximate": opt(js, lambda js: js['Age']['M']['IsApproximate']['BOOL']),
            "AgeGroup": opt(js, lambda js: js['Age']['M']['AgeGroup']['M']['Name']['S'])
       },
       "Campus": js['ContactLocation']['M']['Name']['S'],
       "MainPhoto": opt(js, lambda js: {
              "Photo": js['Photos']['L'][0]['M']['Photo']['S'],
              "PhotoThumbnailFormat": js['Photos']['L'][0]['M']['PhotoThumbnailFormat']['S'],
              "PhotoId": js['Photos']['L'][0]['M']['Id']['N']
       }) 
    } for js in response['Items']]

def opt(js, optionalValueFunction):
    try:
        return optionalValueFunction(js)
    except:
        return None

def lambda_handler(event, context):
    try:
        mq = event['multiValueQueryStringParameters']
        response = query(mq['StatusCategory'], mq['AnimalType'], mq['Location'])
        return {
            'statusCode': 200,
            'body': json.dumps({'request':mq, 'response':response})
        }
    except Exception as e:
        return {
            'statusCode': 200,
            'body':json.dumps({'error': traceback.format_exc()})
        }
