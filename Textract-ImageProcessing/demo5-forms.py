import boto3
from trp import Document
import sys

# Example - "python demo5-forms.py assets/form-sample.png"

# Document
s3BucketName = "ircc-textract-demo"
documentName = str(sys.argv[1])

# Amazon Textract client
textract = boto3.client('textract')

######################################################
# Call Amazon Textract
response = textract.analyze_document(
    Document={
        'S3Object': {
            'Bucket': s3BucketName,
            'Name': documentName
        }
    },
    FeatureTypes=["FORMS"])

doc = Document(response)

######################################################
# Print out the response

for page in doc.pages:
    for field in page.form.fields:
        print("{:>30}  {:>30}".format(field.key, field.value))
