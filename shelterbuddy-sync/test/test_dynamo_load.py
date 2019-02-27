import boto3
from sys import argv
import json
from decimal import Decimal

f = open(argv[1], "r")
animals = json.loads(f.read(), parse_float=Decimal)

dynamodb = boto3.resource('dynamodb', region_name='us-west-1')

table = dynamodb.Table('sdhs.animals')

def scan(var):
    if isinstance(var, dict):
        for k, v in var.items():
            if v is None or v == '' or v == []:
                var[k] = 'n/a'
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

