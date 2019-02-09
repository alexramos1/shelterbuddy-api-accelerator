from credentials import shelterbuddyUrl, username, password
from shelterbuddy import sbauth, sbload
from datetime import datetime, timedelta

token = sbauth(shelterbuddyUrl, username, password)
target = "/api/v2/animal/list?PageSize=100"
cutoff = (datetime.today() - timedelta(days=1)).replace(microsecond=0).isoformat() + "Z"

for animal in sbload(shelterbuddyUrl, token, target, cutoff):
    print(animal['Name'], ' ', animal['Id'])
