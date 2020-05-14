import boto3
import sys

# Example - "python demo2-text-multicolumn.py assets/two-column-image.jpg"

# Document
s3BucketName = "ryanjwaters-textract-demo"
documentName = str(sys.argv[1])

# Amazon Textract client
textract = boto3.client('textract')

######################################################
# Call Amazon Textract

response = textract.detect_document_text(
    Document={
        'S3Object': {
            'Bucket': s3BucketName,
            'Name': documentName
        }
    })

######################################################
# Print out the response

for item in response["Blocks"]:
    if item["BlockType"] == "LINE":
        print ('\033[94m' +  item["Text"] + '\033[0m')
