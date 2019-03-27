import boto3
import json
from boto3.dynamodb.conditions import Key, Attr

def opt(js, optionalValueFunction):
    try:
        return optionalValueFunction(js)
    except:
        return None

class Database:

    dynamodb = boto3.resource('dynamodb', region_name='us-west-1')
    tableName = 'sb-animals'
    table = dynamodb.Table(tableName)
    
    def removeNulls(self, var):
        if isinstance(var, dict):
            for k in list(var.keys()):
                v = var[k]
                if isinstance(v, (dict, list)):
                    self.removeNulls(var[k])
                if v is None or v == [] or v == {} or v == '':
                    del var[k]
        elif isinstance(var, list):
            for d in var:
                self.removeNulls(d)
    
    def save(self,animal):
        animal = {
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
                  "Photo": animal['Photos'][0]['Photo'],
                  "PhotoThumbnailFormat": animal['Photos'][0]['PhotoThumbnailFormat'],
                  "PhotoId": animal['Photos'][0]['Id']
           }) 

        }
        self.removeNulls(animal)
        try:
            self.table.put_item(Item=animal)
            print("STORED: " + str(animal))
        except:
            print(animal)
            raise
        
    def delete(self, animal):
        self.table.delete_item(Key={'Id': animal['Id']})
        print("DELETED: " + str(animal))
    