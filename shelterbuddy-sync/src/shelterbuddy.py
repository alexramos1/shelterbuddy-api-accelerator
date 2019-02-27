from config import filter
from urllib.request import Request, urlopen
import json
from decimal import Decimal

uriCache = {}

def sbauth(shelterbuddyUrl, username, password):
    query = "/api/v2/authenticate?username=" + username + "&password=" + password
    req = Request(shelterbuddyUrl + query);
    req.add_header('Content-Type', 'application/json')
    r = urlopen(req)
    
    if(r.getcode() != 200):
        raise Exception("failed with rc=" + r.getcode())
        
    return json.loads(r.read())

def sbload(shelterbuddyUrl, token, target, cutoff):
    
    postparm = ("{ 'UpdatedSinceUTC':'" + cutoff + "'}").encode('utf-8')

    while target != None:
        
        print(target)
        
        req = Request(shelterbuddyUrl + target, method='POST', data=postparm)
        
        req.add_header("sb-auth-token", token)
        req.add_header("content-type", "application/json")
        
        r = urlopen(req)
        
        if(r.getcode() != 200):
            raise Exception("failed with rc=" + r.getcode())
        
        data = json.loads(r.read(), parse_float=Decimal)
        
        for animal in data['Data']:
            yield animal
        
        target = data['Paging']['Next']

def sbget(shelterbuddyUrl, token, target):
        req = Request(shelterbuddyUrl + target)
        
        req.add_header("sb-auth-token", token)
        req.add_header("content-type", "application/json")
        
        r = urlopen(req)
        
        if(r.getcode() != 200):
            raise Exception("failed with rc=" + r.getcode())
        
        return json.loads(r.read())

def resolve(shelterbuddyUrl, token, uri):
    if not(uri in uriCache):
        uriCache[uri] = sbget(shelterbuddyUrl, token, uri)
    return uriCache[uri]

def process(shelterbuddyUrl, token, animals):
    for animal in animals:
        animal['Status']['UriValue'] = resolve(shelterbuddyUrl, token, animal['Status']['Uri'])
        if 'Name' in animal['Status']['UriValue']:
            del animal['Status']['UriValue']['Name']
        if 'Id' in animal['Status']['UriValue']:
            del animal['Status']['UriValue']['Id'] 
        if(filter(animal)):
            yield animal
