#
# Test the removeNulls() function. Tester must validate the result by visual inspection.
#
import database
from sys import argv
import json
from decimal import Decimal

f = open(argv[1], "r")
animals = json.loads(f.read(), parse_float=Decimal)

db = database.Database()

for animal in animals:
    db.removeNulls(animal)
    print(json.dumps(animal, indent=4))

