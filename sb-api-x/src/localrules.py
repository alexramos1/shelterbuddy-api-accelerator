#
# "Local" rules for pre-processing ShelterBuddy data.
# This is based on the needs of the specific local organization.
#
import config

def applyFilters(sbconn, animals, saveFunction, deleteFunction):
    for animal in animals:
        
        # expand the status variable to allow further filtering
        animal['Status']['UriValue'] = sbconn.fetchUri(animal['Status']['Uri'])

        # cleanup redundant data        
        if 'Name' in animal['Status']['UriValue']:
            del animal['Status']['UriValue']['Name']
        if 'Id' in animal['Status']['UriValue']:
            del animal['Status']['UriValue']['Id']
             
        # Check local filtering rules
        cat = config.categorize(animal)
        print(str(cat) + ' ' + str(animal['Status']['Name']) + ' ' + animal['LastUpdatedUtc'])
         
        if(cat):
            animal['StatusCategory'] = cat
            
            # inline the photo urls
            animal['Photos'] = sbconn.fetchPhotos(animal['Id'])
        
            saveFunction(animal)
            
        else:
            deleteFunction(animal)
