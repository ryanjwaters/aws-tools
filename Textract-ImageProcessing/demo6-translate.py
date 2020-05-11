import boto3
import sys

# Document
s3BucketName = "textract-demo"
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

#print(response)

######################################################
# Call Amazon Translate
translate = boto3.client('translate')

#print ('')
for item in response["Blocks"]:
    if item["BlockType"] == "LINE":
        print ('\033[94m' +  item["Text"] + '\033[0m')
        result = translate.translate_text(Text=item["Text"], SourceLanguageCode="en", TargetLanguageCode="fr")
        print ('\033[92m' + result.get('TranslatedText') + '\033[0m')
    print ('')
