from credentials import shelterbuddyUrl, username, password
from shelterbuddy import ShelterBuddyConnection
from datetime import datetime, timedelta
import json
import config

conn = ShelterBuddyConnection(shelterbuddyUrl, username, password)
target = "/api/v2/animal/list?PageSize=200"
cutoff = (datetime.today() - timedelta(days=config.days)).replace(microsecond=0).isoformat() + "Z"

animals = []

for animal in conn.sbload(target, cutoff):
    #print(animal['Name'], ' ', animal['Id'])    
    animals.append(animal)
    
f = open("animals.json", "w")
f.write(json.dumps(animals))
