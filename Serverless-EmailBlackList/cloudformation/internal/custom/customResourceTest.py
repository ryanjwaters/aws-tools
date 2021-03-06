import boto3
import json
import logging
from botocore.vendored import requests
from botocore.exceptions import ClientError

LOGGER = logging.getLogger()
LOGGER.setLevel(logging.INFO)

def handler(event, context):

    try:
        LOGGER.info('Request received:\n %s', event)
        LOGGER.info('Response received:\n %s', context)

        # Retrieve data from the request
        request_properties = event.get('ResourceProperties', None)
        identity = request_properties['identity']
        snsTopicARN = request_properties['snsTopicARN']

        if event['RequestType'] == 'Create':
            LOGGER.info('Create custom resource: ' +identity+ " : " +snsTopicARN)

            # Create a new SES resource and specify a region.
            client = boto3.client('ses', region_name="us-east-1")
            client.set_identity_notification_topic(Identity=identity, NotificationType='Bounce',    SnsTopic=snsTopicARN)
            client.set_identity_notification_topic(Identity=identity, NotificationType='Complaint', SnsTopic=snsTopicARN)
            client.set_identity_notification_topic(Identity=identity, NotificationType='Delivery',  SnsTopic=snsTopicARN)
            send_response(event, context, "SUCCESS", { "Message": "Resource created" })
        
        elif event['RequestType'] == 'Update':
            LOGGER.info('Update custom resource')
            send_response(event, context, "SUCCESS", { "Message": "Resource updated" })
        
        elif event['RequestType'] == 'Delete':
            LOGGER.info('Delete custom resource')

            client = boto3.client('ses', region_name="us-east-1")
            client.set_identity_notification_topic(Identity=identity, NotificationType='Bounce') #Clear out the SNS usage
            client.set_identity_notification_topic(Identity=identity, NotificationType='Complaint')
            client.set_identity_notification_topic(Identity=identity, NotificationType='Delivery')

            send_response(event, context, "SUCCESS", { "Message": "Resource deleted" })
        
        else:
            LOGGER.info('Unexpected event request received from CFM')
            send_response(event, context, "FAILED", { "Message": "Unexpected event received from CFM" })
    
    except:
        LOGGER.error('Unexpected error during processing', exc_info=True)
        send_response(event, context, "FAILED", { "Message": "Exception during processing" })

def send_response(event, context, response_status, response_data):

    # Save the response in S3 using the responseURL
    try:
        response_body = json.dumps({
            "StackId": event['StackId'],
            "RequestId": event['RequestId'],
            "LogicalResourceId": event['LogicalResourceId'],
            "Status": response_status,
            "Reason": "See CW: " + context.log_stream_name,
            "PhysicalResourceId": context.log_stream_name,
            "Data": response_data
        })

        LOGGER.info("Custom Resource: Sending response %s", response_body)

        headers = {
            'content-type': '',
            'content-length': str(len(response_body))
        }

        response_url = event.get('ResponseURL', None)
        result = requests.put(response_url, data=response_body, headers=headers)
        LOGGER.info("Returned status code: %s", result.reason)
    except Exception as e:
        LOGGER.error("Failed sending response", exc_info=True)
        raise