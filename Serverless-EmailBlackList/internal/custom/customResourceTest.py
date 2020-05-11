import boto3
import json
import random
from botocore.vendored import requests
from collections import namedtuple
from botocore.exceptions import ClientError

def test(ec2TagName):

    try:
        #ec2 = boto3.resource('ec2') #, region_name=Region
        #ec2.create_instances(
        #    ImageId='ami-0323c3dd2da7fb37d',
        #    MinCount=1,
        #    MaxCount=1,
        #    InstanceType='t2.micro')

        return {
            "StatusCode" : 200,
            "Message" : "OK"
        }

    except ClientError as e:
        return {
            "StatusCode" : 400,
            "Message" : e
        }

def handler(event, context):

    # Create variable to hold the response
    print("Custom Resource: Request received")
    print(event)
    for k,v in event.items():
        print(f"Custom Resource: key: {k} value: {v}")
    
    # Retrieve data from the request
    request_type = event.get('RequestType', None)
    resource_type = event.get('ResourceType', None)
    response_url = event.get('ResponseURL', None)
    request_properties = event.get('ResourceProperties', None)
    ec2TagName = request_properties['ec2TagName']

    # These values must be copied to the response
    response_data = {}
    response_data['StackId'] = event.get('StackId', None)
    response_data['RequestId'] = event.get('RequestId', None)
    response_data['LogicalResourceId'] = event.get('LogicalResourceId', "")
    response_data['PhysicalResourceId'] = event.get('PhysicalResourceId', f"{context.function_name}-{context.function_version}")
    response_data['Data'] = {}
    response_data['Reason'] = "More info in CloudWatch"

    answer = test(ec2TagName)

    if answer['StatusCode'] == 400:
        print(f"Custom Resource: FAILED: {answer['Message']}")
        response_data['Status'] = "FAILED"
        response_data['Reason'] = answer['Message']
    else:
        response_data['Status'] = "SUCCESS"
        response_data['Data']['Test'] = answer['Message']
        response_data['Reason'] = answer['Message']

    # Save the response in S3 using the responseURL
    json_response = json.dumps(response_data)
    headers = {
        'content-type': '',
        'content-length': str(len(json_response))
    }

    print("Custom Resource: Sending response")
    print(json_response)

    try:
        result = {}
        result = requests.put(response_url, data=json_response, headers=headers)
        print(f"CloudFormation returned status code: {result.reason}")
    except Exception as e:
        print(f"Failed sending response: error: {e}")
        raise

    # Return the response data
    return response_data