import boto3
import datetime

def demo():

    # Total spend (Monthly)
    query_consumption("2019-12-01", "2020-04-30", "MONTHLY", None, "RECORD_TYPE")

    # Total spend grouped by account (Monthly)
    print("********************************************************")
    query_consumption("2019-12-01", "2020-04-30", "MONTHLY", None, "LINKED_ACCOUNT")

    # Total spend grouped by account (Daily)
    print("********************************************************")
    query_consumption("2020-04-01", "2020-04-30", "DAILY", None, "LINKED_ACCOUNT")

    # Total spend grouped by service (Monthly)
    print("********************************************************")
    query_consumption("2019-12-01", "2020-04-30", "MONTHLY", None, "SERVICE")

    myFilter = get_test_filter()

    # Total spend grouped by account (Monthly) including a test filter for specific services/accounts
    print("********************************************************")
    query_consumption("2019-12-01", "2020-04-30", "MONTHLY", myFilter, "LINKED_ACCOUNT")

    # Total spend grouped by service (Monthly) including a test filter for specific services/accounts
    print("********************************************************")
    query_consumption("2019-12-01", "2020-04-30", "MONTHLY", myFilter, "SERVICE")

def query_consumption(startDate, endDate, granularity, filter, groupByKey):

    client = boto3.client('ce', 'us-east-1')
    nextToken = None
    results = []

    while True:
        if nextToken:
            kwargs = { 'NextPageToken' : nextToken }
        else:
            kwargs = {}

        if filter is None:
            myResults = client.get_cost_and_usage(
                            TimePeriod= { 'Start': startDate, 'End': endDate }, 
                            Granularity= granularity, 
                            Metrics= [ 'UnblendedCost' ],
                            GroupBy= [{ 'Type': 'DIMENSION', 'Key': groupByKey } ],
                            **kwargs)
        else:
            myResults = client.get_cost_and_usage(
                            TimePeriod= { 'Start': startDate, 'End': endDate }, 
                            Granularity= granularity, 
                            Metrics= [ 'UnblendedCost' ],
                            GroupBy= [{ 'Type': 'DIMENSION', 'Key': groupByKey } ],
                            **kwargs)

        # Append results from multiple paginations
        results += myResults['ResultsByTime']

        if 'NextToken' in myResults:
            nextToken = myResults['NextToken']
        else:
            break
    
    for result in results:
        date = result['TimePeriod']['Start']
        estimated = result['Estimated']

        for group in result['Groups']:
            amount = group['Metrics']['UnblendedCost']['Amount']
            unit = group['Metrics']['UnblendedCost']['Unit']

            # Print results
            row = "{:15}.{:<80}{:<20} {}"  # build formatter string
            print(row.format(date, str(group['Keys']), amount, unit))

def get_test_filter():
    return 
    { 
        'And': [ 
            { 
                'Dimensions': { 
                    'Key' : 'SERVICE', 
                    'Values' : [ 'Amazon Route 53', 'AWS CloudTrail' ]
                }
            },
            { 
                'Dimensions': { 
                    'Key': 'LINKED_ACCOUNT', 
                    'Values': [ '396696610383' ] 
                }
            }
        ]
    }

def get_current_date_minus_30_days():
    now = datetime.datetime.utcnow()
    start = (now - datetime.timedelta(days=30)).strftime('%Y-%m-%d')
    end = now.strftime('%Y-%m-%d')
    print("Start= %s , End= %s ", start, end)

def lambda_handler(event, context):
    demo()

# To test from client without running this on AWS lambda
lambda_handler({}, {})