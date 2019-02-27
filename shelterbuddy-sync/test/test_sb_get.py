from credentials import shelterbuddyUrl, username, password
from shelterbuddy import ShelterBuddyConnection
import json
import sys

conn = ShelterBuddyConnection(shelterbuddyUrl, username, password)
target = sys.argv[1]

js = conn.sbget(target)

print(json.dumps(js, indent=4))