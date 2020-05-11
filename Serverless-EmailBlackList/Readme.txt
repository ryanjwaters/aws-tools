aws cloudformation package \
--template-file template.yaml \
--s3-bucket ryanjwaters \
--output-template-file template.packaged.yml

aws cloudformation deploy \
--template-file template.packaged.yml \
--stack-name serverlessDemo \
--capabilities CAPABILITY_NAMED_IAM \
--parameter-overrides Stage=Dev

####################################################################################
# Command line to check the ZIP file 'package' put in S3 (contains the lambda function)
aws s3 ls
aws s3 cp s3://ryanjwaters/0f673636f75acd9d9eb8df83a0348a59 /tmp
unzip -l /tmp/0f673636f75acd9d9eb8df83a0348a59