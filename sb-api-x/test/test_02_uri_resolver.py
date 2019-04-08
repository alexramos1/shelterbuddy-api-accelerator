#
# Test the 2nd step in SB data download:
# Data enrichment by resolving uri refs and photos
#
import json
import sys
from shelterbuddy import ShelterBuddyConnection, DecimalEncoder
from datetime import datetime
import database

f = open(sys.argv[1], "r")
data = json.loads(f.read())[0:9]
conn = ShelterBuddyConnection()
db = database.Database()

conn.resolve(data, 'Uri', lambda uri: conn.fetchUri(uri))
    
f = open("animals-%s-resolved.json" % datetime.today().strftime('%Y-%m-%d'), "w")
f.write(json.dumps(data, cls=DecimalEncoder))
