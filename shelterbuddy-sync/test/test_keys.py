from sys import argv
import json

f = open(argv[1], "r")
data = json.loads(f.read())
dedup = {}

for animal in data:
    atype = animal['Type']['Name']
    loc = animal['ContactLocation']['Name'] 
    if(not animal['Sex'] is None):
        sex = animal['Sex']['Name']
    else:
        sex = 'Unknown'
    status = animal['Status']['Name']
    
    info = atype + ':' + loc + ':' + sex + ':' + status
    if(not(info in dedup)):
        dedup[info] = True
        print(info)
