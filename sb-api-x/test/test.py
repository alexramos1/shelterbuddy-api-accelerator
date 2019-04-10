#
# a super-simple Integration Testing framework for REST Endpoints
#
from urllib.request import urlopen
import os
import json

def test(query, validator):
    url = os.environ['API_URL'] + query
    print(url)
    r = urlopen(url)
    check = json.loads(r.read())
    #print(json.dumps(check, indent=4))
    if(r.info()['Access-Control-Allow-Origin'] != '*'):
        raise Exception("failed test: missing CORS header")
    if(not(validator(check['response']))):
        raise Exception("failed test: validator failed")
    return check
