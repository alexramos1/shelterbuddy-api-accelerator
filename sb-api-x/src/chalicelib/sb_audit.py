
from .database import Database, byline
from .localrules import triageForWeb
from .shelterbuddy import ShelterBuddyConnection
from urllib.error import HTTPError

db = Database()
conn = ShelterBuddyConnection()

def audit():
    for item in db.scan():
        
        keep = None

        try:
            animal = conn.fetchAnimal(item['Id'])
            keep = triageForWeb(animal)
        except HTTPError as e:
            if e.code == 404:
                keep = False
                animal = item
            else:
                raise e
            
        if not keep:
            if not db.delete(animal):
                print('DELETE FAILED FOR %s' % byline(animal))
