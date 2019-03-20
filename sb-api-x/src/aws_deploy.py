import boto3
from zipfile import ZipFile
import os

ZIP = '_lambda_package.zip'
with ZipFile(ZIP, 'w') as myzip:
	myzip.write('sb-search.py')
	
client = boto3.client('lambda', region_name = os.environ['AWS_REGION'])

fn_name = "sb-search"
fn_role = 'arn:aws:iam::' + os.environ['AWS_ACCOUNT'] + ':role/sb-search'

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
	    Handler="{0}.lambda_handler".format(fn_name),
	    Code={'ZipFile': open(ZIP.format(fn_name), 'rb').read(), },
	)
