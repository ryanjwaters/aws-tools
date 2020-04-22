# aws-tools

# You can use SMS to query services available in a particula region, and then also to get human readable service name and AWS marketing URL

- Query services supported in a particular region (ie-"ca-central-1") 
```aws ssm get-parameters-by-path --path /aws/service/global-infrastructure/regions/ca-central-1/services --output json | jq .Parameters[].Name | sort```

- You can query all servies
```aws ssm get-parameters-by-path --path /aws/service/global-infrastructure/services --output json | jq .Parameters[].Name | sort```

- For each of the result above you can query the service name and URL for more information (ie-"athena")
```aws ssm get-parameters-by-path --path /aws/service/global-infrastructure/services/athena --output json | jq .Parameters[].Value```
