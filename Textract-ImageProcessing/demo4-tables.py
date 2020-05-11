import boto3
from trp import Document
import sys

# Example - "python demo4-tables.py assets/table-sample.png"

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
    FeatureTypes=["TABLES"])

doc = Document(response)

######################################################
# Print out the response

for page in doc.pages:
     # Print tables
    for table in page.tables:
        print("-------------------------------------------------------")

        for r, row in enumerate(table.rows):
            if r == 0:
                for c, cell in enumerate(row.cells):
		    print("\tHeader {} - {}".format(c, cell.text))
            else:
                print("\tRow= {}".format(r)),
                for c, cell in enumerate(row.cells):
                    print("\t{}".format(cell.text)),
            print("")
