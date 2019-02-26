from credentials import shelterbuddyUrl, username, password
from shelterbuddy import sbauth, sbget
import json
import sys

token = sbauth(shelterbuddyUrl, username, password)
target = sys.argv[1]

js = sbget(shelterbuddyUrl, token, target)

print(json.dumps(js, indent=4))