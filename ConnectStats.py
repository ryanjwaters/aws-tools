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

cw = boto3.client('cloudwatch')
s3 = boto3.client('s3')

def add_connect_metric_query(connectId, reqId, metricName, stat):
    return  {
        'Id': reqId,
        'MetricStat': {
            'Metric': {
                'Namespace': "AWS/Connect",
                'MetricName' : metricName,
                'Dimensions': [
                    { 'Name': "InstanceId",  'Value' : connectId },
                    { 'Name': "MetricGroup", 'Value' : "VoiceCalls" }
                ]
            },
            'Period': 3600,
            'Stat' : stat,
        },
        'Label': reqId,
        'ReturnData': True
    }

def write_result_file(result_file, results):
    for i in range(len(results['Timestamps'])):
        dateAndTime = results['Timestamps'][i]
        dateAndTimeLocal = convert_timezone_local(dateAndTime)
        dateAndTimeLocalOutput = dateAndTimeLocal.strftime("%Y-%m-%dT%H:00:00")
        result = results['Values'][i]   
        result_file.write("{}\t{}\n".format(dateAndTimeLocalOutput, result))
    result_file.close()

def convert_timezone_local(dateAndTime):
    from_zone = tz.gettz('UTC')
    to_zone = tz.gettz('America/New_York')

    dateAndTime = dateAndTime.replace(tzinfo=from_zone)
    return dateAndTime.astimezone(to_zone)

def convert_timezone_utc(dateAndTime):
    from_zone = tz.gettz('America/New_York')
    to_zone = tz.gettz('UTC')

    dateAndTime = dateAndTime.replace(tzinfo=from_zone)
    return dateAndTime.astimezone(to_zone)

def get_value(event, key):
    try:
        return os.environ[key]  # Lambda environment variable
    except:
        try :
            return event[key] # Event variable
        except:
            return None

def lambda_handler(event, context):

    with tempfile.TemporaryDirectory() as tmpdir:
        connect_id = get_value(event, "CONNECT_ID")
        s3_dest_bucket = get_value(event, "S3_DEST_BUCKET")
        sns_topic = get_value(event, "SNS_TOPIC")

        now = datetime.now()
        print ("Current time \t\t" +now.strftime("%Y-%m-%dT%H:%M:%S"))

        start = datetime.combine(date.today(), datetime.min.time())
        startTime = start.strftime("%Y-%m-01T%H:00:00")
        print("Query start time: \t" +startTime + " UTC")

        nowUTC = convert_timezone_utc(now)
        endTime = nowUTC.strftime("%Y-%m-%dT%H:00:00")
        print("Query end time: \t" +endTime + " UTC\n")

        response = cw.get_metric_data(
            MetricDataQueries = [
                add_connect_metric_query(connect_id, "totalCalls", "CallsPerInterval", "Sum"),
                add_connect_metric_query(connect_id, "concurrentCalls", "ConcurrentCalls", "Maximum")
            ],
            StartTime=startTime,
            EndTime=endTime
        )

        now = datetime.now()
        out_prefix = now.strftime("%Y-%m-%dT%H")
        file_path_concurrentcalls = os.path.join(tmpdir, out_prefix+ "-concurrentCalls.txt")
        file_path_totalcalls = os.path.join(tmpdir, out_prefix+ "-totalCalls.txt")

        metricDataResults = response['MetricDataResults']
        for metricDataResult in metricDataResults:
            id = metricDataResult['Id']
            if id == "concurrentCalls":
                f = open(file_path_concurrentcalls, "w+")
                write_result_file(f, metricDataResult)
                
            elif id == "totalCalls":
                f = open(file_path_totalcalls, "w+")
                write_result_file(f, metricDataResult)

        # Build up a message
        message = "Concurrent calls (Maximum)\n"
        f = open(file_path_concurrentcalls, "r")
        message += f.read()

        message += "\nTotal calls\n"
        f = open(file_path_totalcalls, "r")
        message += f.read()

        print(message)

        # Upload to S3 is a bucket was provided
        if s3_dest_bucket is not None:
            s3.upload_file(file_path_concurrentcalls, s3_dest_bucket, "concurrentCalls.txt")
            s3.upload_file(file_path_totalcalls, s3_dest_bucket, "totalCalls.txt")

        # Send to SNS topic if one was provided (Setup SNS to send email, text, etc)
        if sns_topic is not None:
            sns = boto3.client('sns')
            sns.publish(Message=message, TopicArn=sns_topic)