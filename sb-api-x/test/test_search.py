from urllib.request import urlopen
import os
import json

#r = urlopen(os.environ['API_URL'] + '/search?AnimalType=Cat&Location=Oceanside%20Campus%20-%20Dogs&StatusCategory=available')

r = urlopen(os.environ['API_URL'] + '/search?AnimalType=ALL&Location=Escondido%20Campus&StatusCategory=rescue')
print(json.dumps(json.loads(r.read()), indent=4))