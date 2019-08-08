from urllib.request import Request, urlopen
import urllib
import json
from decimal import Decimal
from os import getenv
from urllib.parse import quote
from docutils.parsers.rst.directives import uri

class ShelterBuddyConnection:
    "Connects to ShelterBuddy API"
    
    uriCache = {}

    def __init__(self, shelterbuddyUrl=None, username=None, password=None):
        if shelterbuddyUrl is None:
            shelterbuddyUrl = getenv("SHELTERBUDDY_API_URL")
            username = quote(getenv("SHELTERBUDDY_API_USER"))
            password = quote(getenv("SHELTERBUDDY_API_PASSWORD"))
        self.shelterbuddyUrl = shelterbuddyUrl
        self.token = self.authenticate(username, password)
    
    def authenticate(self, username, password):
        query = "/api/v2/authenticate?username=" + username + "&password=" + password
        req = Request(self.shelterbuddyUrl + query);
        req.add_header('Content-Type', 'application/json')
        r = urlopen(req)
        return json.loads(r.read())
        
    def loadAnimals(self, target, cutoff, actionFunction, checkpointFunction):
        
        postparm = ("{ 'UpdatedSinceUTC':'" + cutoff + "'}").encode('utf-8')
    
        while target != None:
            
            print(target)
            
            req = Request(self.shelterbuddyUrl + target, method='POST', data=postparm)
            
            req.add_header("sb-auth-token", self.token)
            req.add_header("content-type", "application/json")
            r = urlopen(req)
            
            processedDT = r.info()["x-shelterbuddy-processed-datetimeutc"]
            
            data = json.loads(r.read(), parse_float=Decimal)
            
            actionFunction(data['Data'])
            
            target = data['Paging']['Next']
            try:   
                last = max([animal['LastUpdatedUtc'] for animal in data['Data']])
            except:
                last = cutoff         
                
            print('timestamps: starting=%s, processed=%s, max=%s' % (cutoff, processedDT, last))

            checkpointFunction(target, last, cutoff)
            return last
    
    def fetchUri(self, uri):
        if(uri.startswith("/api/v2/person/")):
            return "blocked"
        if not(uri in self.uriCache):
            req = Request(self.shelterbuddyUrl + uri)
            
            req.add_header("sb-auth-token", self.token)
            req.add_header("content-type", "application/json")

            try:
                r = urlopen(req)
                self.uriCache[uri] = json.loads(r.read())
            except urllib.error.HTTPError as e:
                if(e.code == 404):
                    self.uriCache[uri] = "404-Not-Found"
                else:
                    raise(e)

        return self.uriCache[uri]
    
    def fetchPhotoLinks(self, animalId):
        
        postparam = urllib.parse.urlencode({"AnimalId": animalId})
        print(postparam)
        url = self.shelterbuddyUrl + "/api/v2/animal/photo/list?page=1&pageSize=30"
        req = Request(url, method='POST', data=postparam.encode('utf-8'))
        req.add_header("sb-auth-token", self.token)
        req.add_header("content-type", "application/x-www-form-urlencoded")
        
        r = urlopen(req)
        
        obj = json.loads(r.read(), parse_float=Decimal)

        for photo in obj['Data']:
            del photo['Animal']
        
        return obj['Data']
    
    def fetchPhotoPayload(self, path):
        print('download photo: ' + path)
        return urlopen(Request(self.shelterbuddyUrl + path)).read()

    def resolve(self, var, key, resolver):
        if isinstance(var, dict):
            for k, v in list(var.items()):
                if k == key:
                    var[k + 'Data'] = resolver(v)
                    yield v
                if isinstance(v, (dict, list)):
                    yield from self.resolve(v, key, resolver)
        elif isinstance(var, list):
            for d in var:
                yield from self.resolve(d, key, resolver)
    
class DecimalEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, Decimal):
            return float(o)
        return super(DecimalEncoder, self).default(o)

