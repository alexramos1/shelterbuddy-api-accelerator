import boto3

dynamodb = boto3.resource('dynamodb', region_name='us-west-1')

dynamodb.create_table(
    TableName='sb-animal-details',
    KeySchema=[
        {
            'AttributeName': 'Id',
            'KeyType': 'HASH'  #Partition key
        }
    ],
    AttributeDefinitions=[
        {
            'AttributeName': 'Id',
            'AttributeType': 'N'
        }
    ],
    BillingMode='PAY_PER_REQUEST'
)

dynamodb.create_table(
    TableName='sb-animals',
    KeySchema=[
        {
            'AttributeName': 'Id',
            'KeyType': 'HASH'  #Partition key
        }
    ],
    AttributeDefinitions=[
        {
            'AttributeName': 'Id',
            'AttributeType': 'N'
        },
        {
            'AttributeName': 'StatusCategory',
            'AttributeType': 'S'
        },
        {
            'AttributeName': 'AnimalType',
            'AttributeType': 'S'
        },
        {
            'AttributeName': 'LocationKey',
            'AttributeType': 'S'
        }
    ],
    #BillingMode='PAY_PER_REQUEST',
    ProvisionedThroughput={
        'ReadCapacityUnits': 10,
        'WriteCapacityUnits': 10
    },
    GlobalSecondaryIndexes=[
        {
            'IndexName': 'StatusCategory-AnimalType-index',
            'KeySchema': [
                {
                    'AttributeName': 'StatusCategory',
                    'KeyType': 'HASH'
                },
                {
                    'AttributeName': 'AnimalType',
                    'KeyType': 'RANGE'
                },
            ],
            'Projection': {
                'ProjectionType': 'ALL'
            },
            #'BillingMode': 'PAY_PER_REQUEST',
            'ProvisionedThroughput': {
                'ReadCapacityUnits': 10,
                'WriteCapacityUnits': 10
            }
        },
        {
            'IndexName': 'StatusCategory-LocationKey-index',
            'KeySchema': [
                {
                    'AttributeName': 'StatusCategory',
                    'KeyType': 'HASH'
                },
                {
                    'AttributeName': 'LocationKey',
                    'KeyType': 'RANGE'
                },
            ],
            'Projection': {
                'ProjectionType': 'ALL'
            },
            #'BillingMode': 'PAY_PER_REQUEST',
            'ProvisionedThroughput': {
                'ReadCapacityUnits': 10,
                'WriteCapacityUnits': 10
            }
        }
    ],
)

dynamodb.create_table(
    TableName='sb-sync',
    KeySchema=[
        {
            'AttributeName': 'hashKey',
            'KeyType': 'HASH'  #Partition key
        }
    ],
    AttributeDefinitions=[
        {
            'AttributeName': 'hashKey',
            'AttributeType': 'S'
        }
    ],
    BillingMode='PROVISIONED',
    ProvisionedThroughput={
        'ReadCapacityUnits': 1,
        'WriteCapacityUnits': 1
    },
)
