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
    check = json.loads(r.read())
    #print(json.dumps(check, indent=4))
    if(r.info()['Access-Control-Allow-Origin'] != '*'):
        raise Exception("failed test: missing CORS header")
    if(not(validator(check['response']))):
        raise Exception("failed test: validator failed")
    
test('/search?AnimalType=Cat&Location=ALL&StatusCategory=rescue',
     lambda check: set(['Cat']) == set([animal['AnimalType'] for animal in check]))

test('/search?AnimalType=Dog&Location=ALL&StatusCategory=rescue',
     lambda check: set(['Dog']) == set([animal['AnimalType'] for animal in check]))

test('/search?AnimalType=Cat&AnimalType=Dog&Location=ALL&StatusCategory=rescue',
     lambda check: set(['Cat','Dog']) == set([animal['AnimalType'] for animal in check]))

test('/search?AnimalType=ALL&Location=Escondido%20Campus&StatusCategory=rescue',
     lambda check: set(['Escondido Campus']) == set([animal['Location'] for animal in check]))

test('/search?AnimalType=ALL&Location=Escondido%20Campus&Location=San%20Diego%20Campus%20-%205500&StatusCategory=rescue',
     lambda check: set(['Escondido Campus', 'San Diego Campus - 5500']) == set([animal['Location'] for animal in check]))

test('/search?AnimalType=ALL&Location=ALL&StatusCategory=rescue',
     lambda check: 'In Foster' in [animal['Status'] for animal in check])

test('/search?AnimalType=ALL&Location=ALL&StatusCategory=available',
     lambda check: 'Available For Adoption' in [animal['Status'] for animal in check])

