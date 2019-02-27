from urllib.request import Request, urlopen
import urllib
import json
from decimal import Decimal

class ShelterBuddyConnection:
    "A basic functional proof-of-concept for ShelterBuddy API connectivity."
    
    uriCache = {}
    
    def __init__(self, shelterbuddyUrl, username, password):
        self.shelterbuddyUrl = shelterbuddyUrl
        self.token = self.authenticate(username, password)
        
    def authenticate(self, username, password):
        query = "/api/v2/authenticate?username=" + username + "&password=" + password
        req = Request(self.shelterbuddyUrl + query);
        req.add_header('Content-Type', 'application/json')
        r = urlopen(req)
        return json.loads(r.read())
    
    def fetchPhotos(self, animalId):
        
        postparam = urllib.parse.urlencode({"AnimalId": animalId})
        url = self.shelterbuddyUrl + "/api/v2/animal/photo/list?page=1&pageSize=100"
        req = Request(url, method='POST', data=postparam.encode('utf-8'))
        req.add_header("sb-auth-token", self.token)
        req.add_header("content-type", "application/x-www-form-urlencoded")
        
        r = urlopen(req)
        
        obj = json.loads(r.read(), parse_float=Decimal)
        
        if obj['Data']:
            if 'Animal' in obj['Data']:
                del obj['Data']['Animal'] 
            return obj['Data']
        else:
            return None
    
    def loadAnimals(self, target, cutoff):
        
        postparm = ("{ 'UpdatedSinceUTC':'" + cutoff + "'}").encode('utf-8')
    
        while target != None:
            
            print(target)
            
            req = Request(self.shelterbuddyUrl + target, method='POST', data=postparm)
            
            req.add_header("sb-auth-token", self.token)
            req.add_header("content-type", "application/json")
            
            r = urlopen(req)
            
            data = json.loads(r.read(), parse_float=Decimal)
            
            for animal in data['Data']:
                yield animal
            
            target = data['Paging']['Next']
    
    def fetchUri(self, uri):
        if not(uri in self.uriCache):
            req = Request(self.shelterbuddyUrl + uri)
            
            req.add_header("sb-auth-token", self.token)
            req.add_header("content-type", "application/json")
            
            r = urlopen(req)
            self.uriCache[uri] = json.loads(r.read())

        return self.uriCache[uri]
    