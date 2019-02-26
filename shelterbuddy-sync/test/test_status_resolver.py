from credentials import shelterbuddyUrl, username, password
from shelterbuddy import sbauth, process
import json

f = open("animals.json", "r")
animals = json.loads(f.read())

token = sbauth(shelterbuddyUrl, username, password)
animals = [a for a in process(shelterbuddyUrl, token, animals)]
    
f = open("animals2.json", "w")

f.write(json.dumps(animals, indent=4))
