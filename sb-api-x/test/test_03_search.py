#
# Basic automated test for the search API
#
from test import test

def check_photo(animals):
    for animal in animals:
        try:
            if(animal['MainPhoto']['default'].find('jpg/320-') > 0):
                return True
        except:
            "ignore"
    return False

test1 = test('/search?AnimalType=ALL&Location=ALL&StatusCategory=available',
     lambda check: check_photo(check['response']))

details = [test('/animal?Id=%d' % animal['AnimalId'], lambda ok:True) for animal in test1['response'][0:9] ]

test('/search?AnimalType=Cat&Location=ALL&StatusCategory=rescue',
     lambda check: set(['Cat']) == set([animal['AnimalType'] for animal in check['response']]))

test('/search?AnimalType=Dog&Location=ALL&StatusCategory=rescue',
     lambda check: set(['Dog']) == set([animal['AnimalType'] for animal in check['response']]))

test('/search?AnimalType=Cat&AnimalType=Dog&Location=ALL&StatusCategory=rescue',
     lambda check: set(['Cat','Dog']) == set([animal['AnimalType'] for animal in check['response']]))

test('/search?AnimalType=ALL&Location=Escondido%20Campus&StatusCategory=rescue',
     lambda check: set(['Escondido Campus']) == set([animal['Location'] for animal in check['response']]))

test('/search?AnimalType=ALL&Location=Escondido%20Campus&Location=San%20Diego%20Campus%20-%205500&StatusCategory=rescue',
     lambda check: set(['Escondido Campus', 'San Diego Campus - 5500']) == set([animal['Location'] for animal in check['response']]))

test('/search?AnimalType=ALL&Location=ALL&StatusCategory=rescue',
     lambda check: 'In Foster' in [animal['Status'] for animal in check['response']])

test('/search?AnimalType=ALL&Location=ALL&StatusCategory=available',
     lambda check: 'Available For Adoption' in [animal['Status'] for animal in check['response']])

test('/search?AnimalType=Cat&AnimalType=Dog&Location=Escondido%20Campus&Location=San%20Diego%20Campus%20-%205500&StatusCategory=available',
     lambda check: set(['Escondido Campus', 'San Diego Campus - 5500']) == set([animal['Location'] for animal in check['response']]) and set(['Cat','Dog']) == set([animal['AnimalType'] for animal in check['response']]))
