# Returns a set of attributes for the item of DynamoDB table with the given primary key
import json
import boto3
import logging
from botocore.exceptions import ClientError

logger = logging.getLogger(__name__)
dyn_resource = boto3.resource("dynamodb")
table_name = 'students'
table = dyn_resource.Table(table_name)

result = table.get_item( 
    Key={'student_id': 's003'},
    ConsistentRead=True,
)

if result.get('Item'):
    print(result['Item'])
else:
    print('not found')
