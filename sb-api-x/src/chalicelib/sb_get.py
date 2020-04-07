import boto3
import json

#
# Endpoint for a single animal
#
dynamodb = boto3.client('dynamodb')

def get_animal(animalId):
    print("GET: " + str(animalId))
    response = dynamodb.get_item(TableName='sb-animal-details', Key={'Id': {'N': animalId }})
    return json.loads(response['Item']['rawData']['S'])
