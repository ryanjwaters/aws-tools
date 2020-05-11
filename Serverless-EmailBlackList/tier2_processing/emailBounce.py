import boto3
import json
import os

def handler(event, context):
    dynamoDBTable = os.environ['databaseName']
    msgBody = event['Records'][0]['body']
    emailAddress = msgBody

    # Insert into DynamoDB
    dynamodb = boto3.client('dynamodb')
    result = dynamodb.put_item(
        TableName = dynamoDBTable,
        Item      = { 
            'EmailAddress' : { 'S' : emailAddress }
        }
    )
    
    print(result)