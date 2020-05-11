import boto3
import json
import os

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