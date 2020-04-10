# aws-tools

These are just example snippets of different CLI commands

# Cloudwatch - Query connect metrics

- Query number of 'calls' in 1 hour intervals within a date range
aws cloudwatch get-metric-data --cli-input-json file://./CLI-cloudwatch-connect-calls.json

- Query max number of 'concurrent calls' in 1 hour intervals within a date range
aws cloudwatch get-metric-data --cli-input-json file://./CLI-cloudwatch-connect-concurrentcalls.json
