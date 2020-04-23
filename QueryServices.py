import os
import tempfile
import json
import boto3
import logging
import sys
from datetime import date
from datetime import datetime
from datetime import timedelta
from dateutil import tz

ssm = boto3.client('ssm')

def query_details(my_result):

    head, tail = os.path.split(my_result['ARN'])
    pathId = '/aws/service/global-infrastructure/services/' + tail
    
    # Query AWS SSM for service full name and marketing URL
    details = ssm.get_parameters_by_path(Path = pathId, MaxResults = 10)

    results = details['Parameters']
    for result in results:
        head, tail = os.path.split(result['Name'])
        my_result[tail] = result['Value']

def extract(response):

    results = response['Parameters']

    my_results = []
    for result in results:
        my_result =  {}
        my_result['Name'] = result['Name']
        my_result['ARN']  = result['ARN']

        # Need to do a query for each service to get more details (Full name, URL, etc)
        query_details(my_result)
        my_results.append(my_result)

    return my_results

def lambda_handler(event, context):

    results = []
    regionId = "ca-central-1"
        
    # Query AWS SSM for list of services in this region
    pathId   = "/aws/service/global-infrastructure/regions/" +regionId+ "/services"
    result = ssm.get_parameters_by_path(Path = pathId, MaxResults = 10)
    results += extract(result)

    while result['NextToken'] is not None:
        result = ssm.get_parameters_by_path(Path = pathId, MaxResults = 10, NextToken=result['NextToken'])
        results += extract(result)

        if 'NextToken' not in result:
            break

    i = 1;
    results.sort(key=lambda x: x['longName'], reverse=False)

    for service in results:
        myURL=''
        if 'marketingHomeURL' in service:
            myURL = format(service['marketingHomeURL'])

        row = "{:>4}.{:<60}{:<60}"  # build formatter string
        print(row.format(i, service['longName'], myURL))
 
        i+=1

    return results

#######################################################
# Test locally from python client (not on AWS lambda)
lambda_handler({}, {})
