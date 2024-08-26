# Query a DynamoDB table by using PartiQL statements and an AWS SDK
import json
import boto3
import logging
from botocore.exceptions import ClientError

logger = logging.getLogger(__name__)
dyn_resource = boto3.resource("dynamodb")
table_name = 'students'
table = dyn_resource.Table(table_name)

def run_partiql(statement, param_list):
    try:
        output = dyn_resource.meta.client.execute_statement(
            Statement=statement, 
            Parameters=param_list
        )
    except ClientError as err:
        logger.error(
            "Couldn't execute batch of PartiQL statements. Here's why: %s: %s",
            err.response["Error"]["Code"],
            err.response["Error"]["Message"],
        )
        raise
    else:
        return output

sql = f'SELECT * FROM "{table_name}" WHERE city=? '
parameters = ['台中市']
results=run_partiql(sql,parameters)
print(results['Items'])