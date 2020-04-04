#
# Dump data from SB API into animals.json, to be used by other tests.
# "Run this first"
#
from chalicelib.shelterbuddy import ShelterBuddyConnection, DecimalEncoder
from datetime import datetime, timedelta
import json

conn = ShelterBuddyConnection()
target = "/api/v2/animal/list?PageSize=50"
cutoff = (datetime.today() - timedelta(hours=1)).replace(microsecond=0).isoformat() + "Z"

animals = []

conn.loadAnimals(target, cutoff, animals.extend, lambda x,y,z: None)
    
f = open("test_utils-animals-%s.json" % datetime.today().strftime('%Y-%m-%d'), "w")
f.write(json.dumps(animals, cls=DecimalEncoder))

