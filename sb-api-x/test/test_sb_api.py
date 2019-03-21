#
# Dump data from SB API into animals.json, to be used by other tests.
#
from shelterbuddy import ShelterBuddyConnection
from datetime import datetime, timedelta
import json

conn = ShelterBuddyConnection()
target = "/api/v2/animal/list?PageSize=200"
cutoff = (datetime.today() - timedelta(days=14)).replace(microsecond=0).isoformat() + "Z"

animals = []

for animal in conn.loadAnimals(target, cutoff):
    animals.append(animal)
    
f = open("animals.json", "w")
f.write(json.dumps(animals))
