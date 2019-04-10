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

test('/search?AnimalType=ALL&Location=ALL&StatusCategory=available',
     lambda check: check_photo(check))

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

test('/search?AnimalType=Cat&AnimalType=Dog&Location=Escondido%20Campus&Location=San%20Diego%20Campus%20-%205500&StatusCategory=available',
     lambda check: set(['Escondido Campus', 'San Diego Campus - 5500']) == set([animal['Location'] for animal in check]) and set(['Cat','Dog']) == set([animal['AnimalType'] for animal in check]))
