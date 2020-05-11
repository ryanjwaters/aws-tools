# aws-tools

# Cloudwatch - Query connect metrics

- Query number of 'calls' in 1 hour intervals within a date range  
```aws cloudwatch get-metric-data --cli-input-json file://./CloudWatch-Connect-calls.json```

- Query max number of 'concurrent calls' in 1 hour intervals within a date range  
```aws cloudwatch get-metric-data --cli-input-json file://./CloudWatch-Connect-concurrentcalls.json```
