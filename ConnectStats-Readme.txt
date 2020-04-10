You can run the script within Lambda, or, standalone client.
Just need your Connect instance ID and S3 bucket (examples below)


Option1: Lambda on AWS
- Create a lambda function
- Add two environment variables:
    'CONNECT_ID'     : "4ddb74f2-26b0-4e4e-9a79-50f5b5f02e4c",
    'S3_DEST_BUCKET' : "ryanjohnwaterstest"


Option 2: Run from Client
- Install python3 and boto3
- Add the following to the bottom of the python file:

event = {
    'CONNECT_ID' : "4ddb74f2-26b0-4e4e-9a79-50f5b5f02e4c",
    'S3_DEST_BUCKET' : "ryanjohnwaterstest"
}
lambda_handler(event, {})

- Then run "python ConnectStats.py"
