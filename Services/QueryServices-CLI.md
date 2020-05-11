You can use SMS to query services available in a particular region  

- Query services supported in a particular region (ie-"ca-central-1")  
```aws ssm get-parameters-by-path --path /aws/service/global-infrastructure/regions/ca-central-1/services --output json | jq .Parameters[].Name | sort```

- You can query all servies  
```aws ssm get-parameters-by-path --path /aws/service/global-infrastructure/services --output json | jq .Parameters[].Name | sort```

- For each of the results above you can query the service name and URL for more information (ie-"athena")  
```aws ssm get-parameters-by-path --path /aws/service/global-infrastructure/services/athena --output json | jq .Parameters[].Value```
