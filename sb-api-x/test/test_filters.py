#
# Test the filtering and mapping of animal data received from ShelterBuddy API
#
from shelterbuddy import ShelterBuddyConnection
from localrules import applyFilters
import json

f = open("animals.json", "r")
animals = json.loads(f.read())

conn = ShelterBuddyConnection()
animals = [a for a in applyFilters(conn,animals)]
    
f = open("animals2.json", "w")

f.write(json.dumps(animals, indent=4))
