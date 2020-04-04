import boto3

dynamodb = boto3.resource('dynamodb')

dynamodb.Table('sb-animal-details').delete()

dynamodb.Table('sb-animals').delete()

dynamodb.Table('sb-sync').delete()

dynamodb.Table('sb-config').delete()
