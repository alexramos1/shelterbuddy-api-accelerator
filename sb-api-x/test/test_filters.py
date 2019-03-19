from credentials import shelterbuddyUrl, username, password
from shelterbuddy import ShelterBuddyConnection
from localrules import applyFilters
import json

f = open("animals.json", "r")
animals = json.loads(f.read())

conn = ShelterBuddyConnection(shelterbuddyUrl, username, password)
animals = [a for a in applyFilters(conn,animals)]
    
f = open("animals2.json", "w")

f.write(json.dumps(animals, indent=4))