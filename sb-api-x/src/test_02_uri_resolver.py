#
# Test the 2nd step in SB data download:
# Data enrichment by resolving uri refs and photos
#
import json
import sys
from chalicelib.shelterbuddy import ShelterBuddyConnection, DecimalEncoder
from datetime import datetime
from chalicelib import database

f = open(sys.argv[1], "r")
data = json.loads(f.read())[0:9]
conn = ShelterBuddyConnection()
db = database.Database()

def testResolve(uri):
    out = conn.fetchUri(uri)
    print("resolving: " + uri + " => " + out)
    return out

conn.resolve(data, 'Uri', testResolve)
    
f = open("test_utils-animals-%s-resolved.json" % datetime.today().strftime('%Y-%m-%d'), "w")
f.write(json.dumps(data, cls=DecimalEncoder))
