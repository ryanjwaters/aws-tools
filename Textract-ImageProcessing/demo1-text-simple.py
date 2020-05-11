import boto3
import sys

# Example: "python demo1-text-simple.py assets/simple-document-image.jpg"

# Document
documentName = str(sys.argv[1])

# Read document content
with open(documentName, 'rb') as document:
    imageBytes = bytearray(document.read())

textract = boto3.client('textract')

######################################################
# Call Amazon Textract

response = textract.detect_document_text(Document={'Bytes': imageBytes})

######################################################
# Print out the response

for item in response["Blocks"]:
    if item["BlockType"] == "LINE":
        print ('\033[94m' +  item["Text"] + '\033[0m')
