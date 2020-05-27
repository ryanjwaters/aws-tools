Before creating the Stack with the provided CloudFormation template you need to:

1) Create a paramater store for the SES email already configured and verified on SES
aws ssm put-parameter --name "VerifiedEmail-Dev" --type String --value "ryanjwaters@amazon.com"

![Summary Diagram](https://github.com/ryanjwaters/aws-tools/blob/master/Serverless-EmailBlackList/summary.png)
