from credentials import shelterbuddyUrl, username, password
from shelterbuddy import sbauth, sbget
from datetime import datetime, timedelta
import json
import sys

token = sbauth(shelterbuddyUrl, username, password)
target = sys.argv[1]
cutoff = (datetime.today() - timedelta(days=1)).replace(microsecond=0).isoformat() + "Z"

print(target)
print(sbget(shelterbuddyUrl, token, target))