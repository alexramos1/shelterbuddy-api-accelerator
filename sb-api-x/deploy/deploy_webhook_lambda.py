import boto3
from zipfile import ZipFile
import os

ZIP = '.lambda_package.zip'
with ZipFile(ZIP, 'w') as myzip:
	myzip.write('../src/sb-webhook.py', arcname='sb-webhook.py')
	
client = boto3.client('lambda', region_name = os.environ['AWS_REGION'])

fn_name = "sb-webhook"
fn_role = 'arn:aws:iam::' + os.environ['AWS_ACCOUNT'] + ':role/sb-webhook'

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
	    Timeout=10,
	    MemorySize=1024,
	    Handler="{0}.lambda_handler".format(fn_name),
	    Code={'ZipFile': open(ZIP.format(fn_name), 'rb').read(), },
	    Environment={
        	'Variables': {
            	'SQS_WEBHOOK': os.environ['SQS_WEBHOOK']
	        }
	    }
	)
