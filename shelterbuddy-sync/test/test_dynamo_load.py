import boto3
from decimal import Decimal
from sys import argv
import json

f = open(argv[1], "r")
animals = json.loads(f.read())

dynamodb = boto3.resource('dynamodb', region_name='us-west-1')

table = dynamodb.Table('sdhs.animals')

def scan(var):
    if isinstance(var, dict):
        for k, v in var.items():
            if v is None or v == '' or v == []:
                var[k] = 'n/a'
            if isinstance(v, float):
                var[k] = str(v)
            if isinstance(v, (dict, list)):
                scan(v)
    elif isinstance(var, list):
        for d in var:
            scan(d)

for animal in animals:
    animal['compositeKey'] = animal['ContactLocation']['Name'] + ':' + animal['Type']['Name']
    scan(animal)
    #print(json.dumps(animal, indent=4))
    response = table.put_item(Item=animal)

