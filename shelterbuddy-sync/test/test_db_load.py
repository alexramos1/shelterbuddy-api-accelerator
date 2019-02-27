import database
from sys import argv
import json
from decimal import Decimal

f = open(argv[1], "r")
animals = json.loads(f.read(), parse_float=Decimal)

db = database.Database()
db.saveAll(animals)