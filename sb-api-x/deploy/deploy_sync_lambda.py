import boto3
from zipfile import ZipFile
import os

ZIP = '.lambda_package.zip'
with ZipFile(ZIP, 'w') as myzip:
	myzip.write('../src/sb-sync.py', arcname='sb-sync.py')
	myzip.write('../src/shelterbuddy.py', arcname='shelterbuddy.py')
	myzip.write('../src/database.py', arcname='database.py')
	myzip.write('../src/localrules.py', arcname='localrules.py')
	
client = boto3.client('lambda', region_name = os.environ['AWS_REGION'])

fn_name = "sb-sync"
fn_role = 'arn:aws:iam::' + os.environ['AWS_ACCOUNT'] + ':role/sb-sync'

try:
	client.update_function_code(
	    FunctionName=fn_name,
	    ZipFile= open(ZIP.format(fn_name), 'rb').read(),
	    Publish=True
	)
except:
	client.create_function(
	    FunctionName=fn_name,
	    Runtime='python3.7',
	    Role=fn_role,
	    Timeout=900,
	    MemorySize=1024,
	    Handler="{0}.lambda_handler".format(fn_name),
	    Code={'ZipFile': open(ZIP.format(fn_name), 'rb').read(), },
	)
