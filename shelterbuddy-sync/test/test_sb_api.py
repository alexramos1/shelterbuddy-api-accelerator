from credentials import shelterbuddyUrl, username, password
from shelterbuddy import sbauth, sbload
from datetime import datetime, timedelta
import json
import config

token = sbauth(shelterbuddyUrl, username, password)
target = "/api/v2/animal/list?PageSize=200"
cutoff = (datetime.today() - timedelta(days=config.days)).replace(microsecond=0).isoformat() + "Z"

animals = []

for animal in sbload(shelterbuddyUrl, token, target, cutoff):
    #print(animal['Name'], ' ', animal['Id'])    
    animals.append(animal)
    
f = open("animals.json", "w")
f.write(json.dumps(animals))
