Before creating the Stack with the provided CloudFormation template you need to:

1) Create a paramater store for the SES email already configured and verified on SES
    ```
    aws ssm put-parameter --name "VerifiedEmail-Dev" --type String --value "mytest@gmail.com"
    ```
    
2) This project you can deploy with SAM (2.1) OR with CFM (2.2)

2.1 Use Serverless Application Model (SAM) to build and deploy

    sam build

    sam deploy --parameter-overrides "Stage=Dev"

    
2.2 Use Cloudformation

    aws cloudformation package  \
        --template-file template_cfm.yaml \
        --s3-bucket ryanjwaters \
        --output-template-file template_cfm.packaged.yml

    aws cloudformation deploy \
        --template-file template_cfm.packaged.yml \
        --stack-name serverlessDemo \
        --capabilities CAPABILITY_NAMED_IAM \
        --parameter-overrides Stage=Dev

![Summary Diagram](https://github.com/ryanjwaters/aws-tools/blob/master/Serverless-EmailBlackList/Readme-summary.png)
