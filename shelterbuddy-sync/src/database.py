import boto3
import json
from boto3.dynamodb.conditions import Key, Attr

class Database:

    dynamodb = boto3.resource('dynamodb', region_name='us-west-1')
    
    table = dynamodb.Table('sdhs.animals')
    
    def prepare(self, var):
        if isinstance(var, dict):
            for k in list(var.keys()):
                v = var[k]
                if isinstance(v, (dict, list)):
                    self.prepare(var[k])
                if v is None or v == [] or v == {} or v == '':
                    del var[k]
        elif isinstance(var, list):
            for d in var:
                self.prepare(d)
    
    def saveAll(self,animals):
        for animal in animals:
            animal['compositeKey'] = animal['ContactLocation']['Name'] + ':' + animal['Type']['Name']
            self.prepare(animal)
            self.table.put_item(Item=animal)
    
    def put(self, k, v):
        self.table.put_item(Item={ 'compositeKey': k, 'Id': 0, 'info': v })

    def get(self, k):
        return self.table.query(KeyConditionExpression=Key('compositeKey').eq(k))
    