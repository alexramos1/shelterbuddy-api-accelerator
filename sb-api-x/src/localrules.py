#
# "Local" rules for pre-processing ShelterBuddy data.
# These rules are customized based on the needs of the specific local organization.
#
import boto3
client = boto3.client('dynamodb', region_name = 'us-west-1')

lost = [
    "Lost",
    "Hold For Possible Match",
    "Possible Match"
]

found1 = [
    "Found",
    "Deceased"
]
found2 = [
    "Available for Adoption - Waiting Space",
    "Available For Adoption",
    "Available for Adoption - In Foster",
    "Hold For Possible Match",
    "Stray - In Foster",
    "Stray Hold",
    "Stray Hold - Awaiting transfer",
    "Stray Hold - In Vet Care",
    "ID Trace",
    "Euthanized During Stray Hold Time"
]

available = [
    "Available For Adoption",
    "Available for Adoption - Awaiting Spay/Neuter",
    "Available for Adoption - In Foster",
    "Available for Adoption - Offsite",
    "Available for Adoption - Waiting Space",
]

# the rescue status list has been moved to dynamo becaused it changes too often
response = client.get_item(TableName='sb-config', Key={ 'section': { 'S': 'rescue' }})
rescue = [item['S'] for item in response['Item']['status']['L']]

def categorize(animal):
    st = animal['Status']['Name']
    if(st in lost and animal['Intake']['Source'] and animal['Intake']['Source']['Name'] == "Found"):
        return "lost"
    elif(st in available):
        return "available"
    elif(st in rescue):
        return "rescue"
    elif(st in found1 and animal['Intake']['Source'] and animal['Intake']['Source']['Name'] == "Found" ):
        return "found"
    elif(st in found2 and animal['Intake']['Source']['Name'] in [ "ACO Impound", "Ambulance", "Stray", "Transfer In" ]):
        return "found"
    else:
        return None 

#
# determine whether an animal should be kept on the website
#
def triageForWeb(animal):
    
    # Check local filtering rules
    ctg = categorize(animal)
     
    if(ctg):
        animal['StatusCategory'] = ctg        
        # keeper
        return True
        
    else:
        # not for website
        return False
