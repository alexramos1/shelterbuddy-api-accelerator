#
# An AWS Lambda function to periodically pre-load Shelterbuddy API data into a DynamoDB table.
#
from shelterbuddy import ShelterBuddyConnection
from database import Database
from credentials import shelterbuddyUrl, username, password
from datetime import datetime, timedelta
from localrules import applyFilters
import json
import config

db = Database()
conn = ShelterBuddyConnection(shelterbuddyUrl, username, password)

info = db.get('_continuation')
if(info['Items']):
    print(info)
    (target,cutoff) = info['Items'][0]['info'].split('#')
else:
    target = "/api/v2/animal/list?PageSize=200"
    cutoff = (datetime.today() - timedelta(days=config.days)).replace(microsecond=0).isoformat() + "Z"
    
action = lambda animals: applyFilters(conn,animals, db.save, db.delete)
persist = lambda target: db.put('_continuation', (target + '#' + cutoff) if target else None)

for animal in conn._loadAnimals(target, cutoff, action, persist):
    print(animal['Id'])
