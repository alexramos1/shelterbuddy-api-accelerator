#
# "Local" rules for pre-processing ShelterBuddy data.
# This is based on the needs of the specific local organization.
#
import config

def applyFilters(sbconn, animals):
    for animal in animals:
        
        # expand the status variable to allow further filtering
        animal['Status']['UriValue'] = sbconn.fetchUri(animal['Status']['Uri'])

        # cleanup redundant data        
        if 'Name' in animal['Status']['UriValue']:
            del animal['Status']['UriValue']['Name']
        if 'Id' in animal['Status']['UriValue']:
            del animal['Status']['UriValue']['Id']
             
        # Check local filtering rules
        if(config.filter(animal)):
            
            # inline the photo urls
            animal['Photos'] = sbconn.fetchPhotos(animal['Id'])
        
            yield animal
