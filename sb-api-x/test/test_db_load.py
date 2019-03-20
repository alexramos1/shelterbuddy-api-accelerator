import database
from sys import argv
import json
from decimal import Decimal
import localrules
from shelterbuddy import ShelterBuddyConnection

f = open(argv[1], "r")
animals = json.loads(f.read(), parse_float=Decimal)

db = database.Database()
conn = ShelterBuddyConnection()

action = lambda animals: localrules.applyFilters(conn,animals, db.save, db.delete)

action(animals)
