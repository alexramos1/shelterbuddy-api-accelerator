import boto3
import json
import traceback

#
# Endpoint for a single animal
#

dynamodb = boto3.client('dynamodb', region_name = 'us-west-1')

def lambda_handler(event, context):
    try:
        mq = event['multiValueQueryStringParameters']
        response = dynamodb.get_item(TableName='sb-animal-details', Key={'Id': {'N': mq['Id'][0] }})
        data = json.loads(response['Item']['rawData']['S'])
        return {
            'statusCode': 200,
            'headers': { 'Access-Control-Allow-Origin': '*' },
            'body': json.dumps({'request':mq, 'response': data })
        }
    except Exception as e:
        return {
            'statusCode': 200,
            'headers': { 'Access-Control-Allow-Origin': '*' },
            'body':json.dumps({'error': traceback.format_exc()})
        }

if __name__ == "__main__":
    import sys
    resp=lambda_handler({'multiValueQueryStringParameters': { 'Id': [ sys.argv[1] ]} }, None)
    print(json.dumps(resp, indent=4))
