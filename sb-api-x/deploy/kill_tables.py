import boto3

dynamodb = boto3.resource('dynamodb', region_name='us-west-1')

try:
    dynamodb.Table('sb-animal-details').delete()
except:
    None

try:
    dynamodb.Table('sb-animals').delete()
except:
    None

try:
    dynamodb.Table('sb-sync').delete()
except:
    None
