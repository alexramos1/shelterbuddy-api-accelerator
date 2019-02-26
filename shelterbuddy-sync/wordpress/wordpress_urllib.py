from requests.auth import HTTPBasicAuth
import requests
import json
import urllib

def create(endpoint, content):
    
    #        'date_gmt': datetime.now().replace(microsecond=0).isoformat() + 'Z',
    url = endpoint['url']
    username = endpoint['username']
    password = endpoint['password']
    params = {
        'title': 'The Title',
        'content': content,
        'exerpt': 'blah'
    }

    postparam = json.dumps(params).encode('utf-8')
    
    password_mgr = urllib.request.HTTPPasswordMgrWithDefaultRealm()
    password_mgr.add_password(None, url, username, password)
    handler = urllib.request.HTTPBasicAuthHandler(password_mgr)
    opener = urllib.request.build_opener(handler)
    
    req = urllib.request.Request(url + '/wp-json/wp/v2/posts', method='POST', data=postparam)
    req.add_header('Content-Type', 'application/json')
    
    r = opener.open(req)
    
    if(r.getcode() != 200):
        raise Exception('failed with rc=' + r.getcode()) 
       
    return json.loads(r.read())
