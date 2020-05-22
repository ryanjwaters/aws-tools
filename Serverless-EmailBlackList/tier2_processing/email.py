import boto3
import json
import logging
import os
from botocore.exceptions import ClientError

LOGGER = logging.getLogger()
LOGGER.setLevel(logging.INFO)

CONFIGURATION_SET = "TestConfigSet"
AWS_REGION = "us-east-1" #TODO: Is this needed, will it default to my region?
SUBJECT = "Amazon SES Test"
CHARSET = "UTF-8"

BODY_TEXT = ("Amazon SES Test \r\n"
    "This email was sent with Amazon SES")
        
BODY_HTML = """<html>
    <head></head>
    <body>
    <h1>Amazon SES Test</h1>
    <p>This email was sent with
    <a href='https://aws.amazon.com/ses/'>Amazon SES</a></p>
    </body>
    </html>
    """   

def sendEmail(toEmailAddress):

    try:
        toEmailAddresses = []
        toEmailAddresses.append(toEmailAddress)
        
        # Get the from email address (from param store)
        ssm = boto3.client('ssm')
        parameter = ssm.get_parameter(Name='VerifiedEmail-Dev') #TODO: Read 'dev' as env variable
        fromEmailAddress = parameter['Parameter']['Value']
        
        # Create a new SES resource and specify a region.
        client = boto3.client('ses', region_name=AWS_REGION)
        
        #Provide the contents of the email.
        response = client.send_email(
            Destination={
                'ToAddresses': toEmailAddresses,
            },
            Message={
                'Body': {
                    'Html': {
                        'Charset': CHARSET,
                        'Data': BODY_HTML,
                    },
                    'Text': {
                        'Charset': CHARSET,
                        'Data': BODY_TEXT,
                    },
                },
                'Subject': {
                    'Charset': CHARSET,
                    'Data': SUBJECT,
                },
            },
            Source=fromEmailAddress
            #ConfigurationSetName=CONFIGURATION_SET
        )
    except ClientError as e:
        LOGGER.info(e.response['Error']['Message'])
    else:
        LOGGER.info("Email sent.  Message ID: "),
        LOGGER.info(response['MessageId'])

def handler(event, context):
    dynamoDBTable = os.environ['databaseName']
    msgBody = event['Records'][0]['body']
    emailAddress = msgBody

    # Get from DynamoDB
    dynamodb = boto3.client('dynamodb')
    result = dynamodb.get_item(
        TableName = dynamoDBTable,
        Key       = { 'EmailAddress' : { 'S' : emailAddress } },
        ReturnConsumedCapacity='TOTAL'
    )
    LOGGER.info(result)

    # Check if the emailAddress is in the black list
    if 'Item' in result:
        item = result['Item']
        LOGGER.info("Email is in the blacklist, cannot send")
        LOGGER.info(item)
    else:
        LOGGER.info("Email is NOT in the blacklist, ok to send")
        sendEmail(emailAddress)