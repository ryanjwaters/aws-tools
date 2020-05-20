import boto3
import json
import os
from botocore.exceptions import ClientError

def sendEmail(toEmailAddress):
    SENDER = "ryanws@amazon.com"
    RECIPIENT = toEmailAddress,
    CONFIGURATION_SET = "TestConfigSet"
    AWS_REGION = "us-east-1"
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
    
    # Create a new SES resource and specify a region.
    client = boto3.client('ses', region_name=AWS_REGION)

    # Try to send the email.
    try:
        #Provide the contents of the email.
        response = client.send_email(
            Destination={
                'ToAddresses': RECIPIENT,
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
            Source=SENDER
            #ConfigurationSetName=CONFIGURATION_SET
        )
    except ClientError as e:
        print(e.response['Error']['Message'])
    else:
        print("Email sent.  Message ID: "),
        print(response['MessageId'])

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
    print(result)

    # Check if the emailAddress is in the black list
    if 'Item' in result:
        item = result['Item']
        print("Email is in the blacklist, cannot send")
        print(item)
    else:
        print("Email is NOT in the blacklist, ok to send")
        sendEmail(emailAddress)