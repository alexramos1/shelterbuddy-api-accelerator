from requests.auth import HTTPBasicAuth
import requests
import json

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
    r = requests.post(url + '/wp-json/wp/v2/posts', 
                      auth=HTTPBasicAuth(username, password), 
                      data=json.dumps(params), 
                      headers={'content-type': 'application/json'})

    if(not(r.ok)):
        raise Exception('failed with rc=' + r.status_code)
        
    return json.loads(r.text)
