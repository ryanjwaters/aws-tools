import boto3
import json
import os

def handler(event, context):
    
    dynamoDBTable = os.environ['databaseName']
    msgBody = event['Records'][0]['body']
    parsedBody = json.loads(msgBody)

    msg = parsedBody['Message']
    parsedMsg = json.loads(msg)
    notificationType = parsedMsg['notificationType']
    emailAddress = parsedMsg['delivery']['recipients'][0]
    print(notificationType + " : " + emailAddress)
    
    # Insert into DynamoDB
    dynamodb = boto3.client('dynamodb')
    result = dynamodb.put_item(
        TableName = dynamoDBTable,
        Item      = { 
            'EmailAddress' : { 'S' : emailAddress }
        }
    )
    
    print(result)