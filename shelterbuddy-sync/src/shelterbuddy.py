from config import filter
from urllib.request import Request, urlopen
import json
from decimal import Decimal

class ShelterBuddyConnection:
    
    uriCache = {}
    
    def __init__(self, shelterbuddyUrl, username, password):
        self.shelterbuddyUrl = shelterbuddyUrl
        self.token = self.sbauth(username, password)
        
    def sbauth(self, username, password):
        query = "/api/v2/authenticate?username=" + username + "&password=" + password
        req = Request(self.shelterbuddyUrl + query);
        req.add_header('Content-Type', 'application/json')
        r = urlopen(req)
        
        if(r.getcode() != 200):
            raise Exception("failed with rc=" + r.getcode())
            
        return json.loads(r.read())
    
    def sbload(self, target, cutoff):
        
        postparm = ("{ 'UpdatedSinceUTC':'" + cutoff + "'}").encode('utf-8')
    
        while target != None:
            
            print(target)
            
            req = Request(self.shelterbuddyUrl + target, method='POST', data=postparm)
            
            req.add_header("sb-auth-token", self.token)
            req.add_header("content-type", "application/json")
            
            r = urlopen(req)
            
            if(r.getcode() != 200):
                raise Exception("failed with rc=" + r.getcode())
            
            data = json.loads(r.read(), parse_float=Decimal)
            
            for animal in data['Data']:
                yield animal
            
            target = data['Paging']['Next']
    
    def sbget(self, target):
            req = Request(self.shelterbuddyUrl + target)
            
            req.add_header("sb-auth-token", self.token)
            req.add_header("content-type", "application/json")
            
            r = urlopen(req)
            
            if(r.getcode() != 200):
                raise Exception("failed with rc=" + r.getcode())
            
            return json.loads(r.read())
    
    def resolve(self, uri):
        if not(uri in self.uriCache):
            self.uriCache[uri] = self.sbget(uri)
        return self.uriCache[uri]
    
    def process(self, animals):
        for animal in animals:
            animal['Status']['UriValue'] = self.resolve(animal['Status']['Uri'])
            if 'Name' in animal['Status']['UriValue']:
                del animal['Status']['UriValue']['Name']
            if 'Id' in animal['Status']['UriValue']:
                del animal['Status']['UriValue']['Id'] 
            if(filter(animal)):
                yield animal
