from urllib.request import Request, urlopen
from datetime import datetime
from base64 import b64encode

import json

def create(endpoint, content):
    
    #        'date_gmt': datetime.now().replace(microsecond=0).isoformat() + 'Z',
    params = {
        'status': 'publish',
        'title': 'The Title',
        'content': content
    }
    postparam = json.dumps(params).encode('utf-8')
    req = Request(endpoint['url'] + '/wp-json/wp/v2/posts', method='POST', data=postparam)
    req.add_header('Content-Type', 'application/json')
    
    creds = endpoint['username'] + ':' + endpoint['password']
    auth  = 'Basic ' + str(b64encode(creds.encode('utf-8')), 'utf-8')
    req.add_header('Authorization', auth)
    
    r = urlopen(req)
    
    if(r.getcode() != 200):
        raise Exception('failed with rc=' + r.getcode())
        
    return json.loads(r.read())
