from urllib.request import Request, urlopen
import json

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
        
        req = Request(shelterbuddyUrl + target, method='POST', data=postparm)
        
        req.add_header("sb-auth-token", token)
        req.add_header("content-type", "application/json")
        
        r = urlopen(req)
        
        if(r.getcode() != 200):
            raise Exception("failed with rc=" + r.getcode())
        
        data = json.loads(r.read())
        
        for animal in data['Data']:
            yield animal
        
        target = data['Paging']['Next']
