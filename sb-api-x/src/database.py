import boto3
import json
from boto3.dynamodb.conditions import Key, Attr

def opt(js, optionalValueFunction, defaultValue = None):
    try:
        return optionalValueFunction(js)
    except:
        return defaultValue

def removeNulls(var):
    if isinstance(var, dict):
        for k in list(var.keys()):
            v = var[k]
            if isinstance(v, (dict, list)):
                removeNulls(var[k])
            if v is None or v == [] or v == {} or v == '':
                del var[k]
    elif isinstance(var, list):
        for d in var:
            removeNulls(d)
    return var

def searchableFields(animal):
    return {
       "Id": animal['Id'],
       "AnimalType": animal['Type']['Name'],
       "LocationKey": animal['ContactLocation']['Name'],
       "Status": animal['Status']['Name'],
       "StatusCategory": animal['StatusCategory'],
       "Name": opt(animal, lambda js: js['Name'].strip()),
       "Sex": opt(animal, lambda js: js['Sex']['Name']),
       "Breed": {
            "Primary": opt(animal, lambda js: js['Breed']['Primary']['Name']),
            "Secondary": opt(animal, lambda js: js['Breed']['Secondary']['Name']),
            "IsCrossBreed": opt(animal, lambda js: js['Breed']['IsCrossBreed'])
       },
       "Age": {
            "Years": opt(animal, lambda js: int(js['Age']['Years'])),
            "Months": opt(animal, lambda js: int(js['Age']['Months'])),
            "Weeks": opt(animal, lambda js: int(js['Age']['Weeks'])),
            "IsApproximate": opt(animal, lambda js: js['Age']['IsApproximate']),
            "AgeGroup": opt(animal, lambda js: js['Age']['AgeGroup']['Name'])
       },
       "MainPhoto": opt(animal, lambda js: {
              "Photo": animal['Photos'][0].values()
       }),
       #"Intake": animal['Intake']['DateUtc'] 
    }
    
class Database:

    dynamodb = boto3.resource('dynamodb', region_name='us-west-1')
    tableName = 'sb-animals'
    table = dynamodb.Table(tableName)
    
    def save(self,animal):
        print('INCOMING: ' + str(animal))
        animal = searchableFields(animal)
        removeNulls(animal)
        try:
            self.table.put_item(Item=animal)
            print("STORED: " + str(animal))
        except:
            print("FAILED:" + str(animal))
            raise
        
    def delete(self, animal):
        try:
            self.table.delete_item(Key={'Id': animal['Id']})
            print("DELETED: " + str(animal))
        except:
            print("SKIPPED: " + str(animal))
    
