#
# Basic automated test for the search API
#
from urllib.request import urlopen
import os
import json

def test(query, validator):
    url = os.environ['API_URL'] + query
    print(url)
    r = urlopen(url)
    data = json.loads(r.read())
    #print(json.dumps(data, indent=4))
    if(r.info()['Access-Control-Allow-Origin'] != '*'):
        raise Exception("failed test: missing CORS header")
    if(not(validator(data['response']))):
        raise Exception("failed test: validator failed")
    
test('/search?AnimalType=Cat&Location=ALL&StatusCategory=rescue',
     lambda data: set(['Cat']) == set([animal['AnimalType'] for animal in data]))

test('/search?AnimalType=Dog&Location=ALL&StatusCategory=rescue',
     lambda data: set(['Dog']) == set([animal['AnimalType'] for animal in data]))

test('/search?AnimalType=ALL&Location=Escondido%20Campus&StatusCategory=rescue',
     lambda data: set(['Escondido Campus']) == set([animal['Location'] for animal in data]))

