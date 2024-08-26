# Query a DynamoDB table by using PartiQL statements and an AWS SDK
import json
import boto3
import logging
from botocore.exceptions import ClientError

logger = logging.getLogger(__name__)
dyn_resource = boto3.resource("dynamodb")
table_name = 'students'
table = dyn_resource.Table(table_name)


results = table.scan(
    FilterExpression="#city = :v1",
    ExpressionAttributeNames={'#city': 'city'},
    ExpressionAttributeValues={
        ':v1': '台中市'
    }
)
if len(results['Items'])>0:
    print(results['Items'])
else:
    print('not found')
