import boto3
import os

apiName = 'sbx'

def createResources(pathPart, function, role):
    
    response = client.create_resource(
        restApiId=apiId,
        parentId=rootId,
        pathPart=pathPart
    )
    print(response)
    resId = response['id']
    
    print("resourceId = " + resId)
    
    response = client.put_method(
        restApiId = apiId,
        resourceId = resId,
        httpMethod = 'ANY',
        authorizationType = 'NONE'
    )
    print(response)
    
    functionArn = 'arn:aws:lambda:us-west-1:%s:function:%s' % (os.environ['AWS_ACCOUNT'], function)
    
    response = client.put_integration(
        restApiId=apiId,
        resourceId=resId,
        httpMethod = 'ANY',
        type='AWS_PROXY',
        timeoutInMillis=8000,
        integrationHttpMethod = 'POST',
        uri = 'arn:aws:apigateway:us-west-1:lambda:path/2015-03-31/functions/%s/invocations' % functionArn,
        passthroughBehavior="WHEN_NO_MATCH",
        contentHandling='CONVERT_TO_TEXT',
        #credentials='arn:aws:iam::' + os.environ['AWS_ACCOUNT'] + ':role/' + role     
    )
    print(response)
    
    response = client.put_integration_response(
        restApiId  = apiId,
        resourceId = resId,
        httpMethod = 'ANY',
        statusCode = '200',
        responseTemplates = {'application/json': ''}
    )
    print(response)
    
    response = client.put_method_response(
        restApiId=apiId,
        resourceId=resId,
        httpMethod = 'ANY',
        statusCode='200'
    )
    print(response)

#
# main
#

client = boto3.client('apigateway', region_name='us-west-1')

apiId = None

response = client.get_rest_apis()
for api in response['items']:
    if(api['name'] == apiName):
        #client.delete_rest_api(restApiId=api['id'])
        apiId = api['id']
    
if(apiId is None):
    response = client.create_rest_api(
        name=apiName,
        description='ShelterBuddy API',
        version='1.0',
        binaryMediaTypes=[
            'image/jpeg',
        ],
        endpointConfiguration={
            'types': [ 'REGIONAL' ]
        }
    )
    print(response)
    
    apiId = response['id']

print("apiId = " + apiId)

response = client.get_resources(restApiId=apiId)
rootId = response['items'][0]['id']
print("rootId = " + rootId)

for res in response['items']:
    if(res['path'] != '/'):
        client.delete_resource(restApiId=apiId, resourceId=res['id'])
        print('deleted resource with id=%s, path=%s' % (res['id'], res['path']))

createResources('animal', 'sb-get', 'sb-search')
createResources('search', 'sb-search', 'sb-search')
createResources('webhook', 'sb-webhook', 'sb-webhook')


