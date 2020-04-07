import boto3
import json
from .shelterbuddy import DecimalEncoder

def byline(animal):
    try:
        return "[%s %s %s %s %s]" % (animal['Name'], animal['Type']['Name'], animal['Id'], animal['Status']['Name'], animal['LastUpdatedUtc'])
    except:
        return json.dumps(animal, cls=DecimalEncoder)

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
       "MainPhoto": opt(animal, lambda js: 
              animal['Photos'][0]
       ),
       "Intake": animal['Intake']['DateUtc'] 
    }
    
class Database:

    SEARCH_TABLE_NAME = 'sb-animals'

    dynamodb = boto3.resource('dynamodb')
    searchTable = dynamodb.Table(SEARCH_TABLE_NAME)
    detailTable = dynamodb.Table('sb-animal-details')
    
    def save(self,animal):
        try:
            searchableData = removeNulls(searchableFields(animal))
            searchableData['LastUpdatedUtc'] = animal['LastUpdatedUtc']
            response = self.searchTable.put_item(Item=searchableData, 
                                                 ConditionExpression="attribute_not_exists(LastUpdatedUtc) OR LastUpdatedUtc <= :LastUpdatedUtc",
                                                 ExpressionAttributeValues={':LastUpdatedUtc':searchableData['LastUpdatedUtc']})
            
            self.detailTable.put_item(Item={'Id': animal['Id'], 'rawData': json.dumps(animal, cls=DecimalEncoder) })
            print("STORED: " + byline(animal))
        except self.dynamodb.meta.client.exceptions.ConditionalCheckFailedException:
            print("WARNING: update skipped - not going to overwrite newer record: " + byline(animal))
        except:
            print("STORE FAILED:" + byline(animal))
            raise
        
    def delete(self, animal):
        try:
            self.searchTable.delete_item(Key={'Id': animal['Id']})
            self.detailTable.delete_item(Key={'Id': animal['Id']})
            print("DELETED: " + byline(animal))
            return True
        except:
            return False
    
    def scan(self):

        LastEvaluatedKey = None
        
        while True:
            
            if LastEvaluatedKey:
                response = self.detailTable.scan(Select='ALL_ATTRIBUTES', Limit=100, ExclusiveStartKey=LastEvaluatedKey)
            else:
                response = self.detailTable.scan(Select='ALL_ATTRIBUTES', Limit=100)

            for item in response['Items']:
                yield json.loads(item['rawData'])

            if 'LastEvaluatedKey' not in response:
                return

            LastEvaluatedKey = response['LastEvaluatedKey']
