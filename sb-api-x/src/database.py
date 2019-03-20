import boto3
import json
from boto3.dynamodb.conditions import Key, Attr

class Database:

    dynamodb = boto3.resource('dynamodb', region_name='us-west-1')
    table = dynamodb.Table('sdhs_animals')
    
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
    
    def save(self,animal):
        animal['LocationKey'] = animal['ContactLocation']['Name']
        animal['AnimalType'] = animal['Type']['Name']
        self.prepare(animal)
        try:
            self.table.put_item(Item=animal)
        except:
            print(animal)
            raise
        
    def delete(self, animal):
        self.table.delete_item(Key={'Id': animal['Id']})
    