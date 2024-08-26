import io
import json
import boto3
import pandas as pd
from botocore.exceptions import ClientError
import logging
import time

dyn_resource = boto3.resource("dynamodb")
logger = logging.getLogger(__name__)
s3_client = boto3.client("s3")
S3_BUCKET_NAME = 'aiotnawscloud0821'
dest_table_name = 'students'
object_key = "student_info.xlsx"  # replace object key

# check the table whether exists
def exists(dynamodb, table_name):
    try:
        table = dynamodb.Table(table_name)
        table.load()
        exists = True
    except ClientError as err:
        if err.response["Error"]["Code"] == "ResourceNotFoundException":
            exists = False
        else:
            logger.error(
                "Couldn't check for existence of %s. Here's why: %s: %s",
                table_name,
                err.response["Error"]["Code"],
                err.response["Error"]["Message"],
            )
            raise
    return exists

# CreateTable, https://docs.aws.amazon.com/amazondynamodb/latest/APIReference/API_CreateTable.html#API_CreateTable_RequestSyntax
def create_table(dynamodb = None, table_name = None):
  try:
    if not dynamodb:
        dynamodb = boto3.resource('dynamodb')
    table = ''
    if not exists(dynamodb, table_name):
        table = dynamodb.create_table(
            TableName = table_name,
            BillingMode =  "PAY_PER_REQUEST",
            KeySchema = [
                {
                    'AttributeName': 'student_id',
                    'KeyType': 'HASH'  # Partition key
                }
            ],
            AttributeDefinitions=[
                {
                    'AttributeName': 'student_id',
                    'AttributeType': 'S'
                }
            ]    
        )
  except ClientError as err:
    logger.error(
        "Couldn't create table %s. Here's why: %s: %s",
        table_name,
        err.response["Error"]["Code"],
        err.response["Error"]["Message"],
    )
    raise
  else:
    return table

# step 1. read excel from S3 object
file_content = s3_client.get_object(Bucket=S3_BUCKET_NAME, Key=object_key)["Body"].read()
df = pd.read_excel(io.BytesIO(file_content), dtype=str, engine='openpyxl')
items = df.to_dict(orient='records') # convert to dictionary

# step 2. Create DynamoDB table and wait for completion
create_table(dyn_resource, dest_table_name)
print('Creating DynamoDB table and wait for completion')
time.sleep(15)

# step 3. write data to Dynamodb in batch mode    
dest_table = dyn_resource.Table(dest_table_name)
try:        
    with dest_table.batch_writer() as writer:
        for item in items:
            writer.put_item(Item=item)
except ClientError:
    logger.exception("Couldn't load data into table %s.", dest_table.name)

