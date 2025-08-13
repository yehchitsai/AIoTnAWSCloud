import json
import boto3
from boto3.dynamodb.conditions import Key, Attr
from botocore.exceptions import ClientError
import logging

logger = logging.getLogger(__name__)
dyn_resource = boto3.resource("dynamodb")
detect_table_name = 'detect_result_table'
detect_table = dyn_resource.Table(detect_table_name)

def lambda_handler(event, context):
  result = {"status":"fail"}
  requestMethod = event['httpMethod']
  if requestMethod=='POST':
    # 查詢辨識記錄
    try:
        requestBody = json.loads(event['body'])
        result["status"] = "fail-參數有誤"
        if requestBody.get('start_time') and requestBody.get('end_time'):
            start_time = requestBody['start_time']
            end_time = requestBody['end_time']
            attr = Attr('date_time')
            response = detect_table.scan(
                FilterExpression=attr.between(start_time, end_time)
            )
            result["status"] = "success"
            result['results'] = response['Items']

    except ClientError as err:
        logger.error(
            "查詢辨識記錄失敗. Here's why: %s: %s",
            err.response["Error"]["Code"],
            err.response["Error"]["Message"],
        )  
        result["status"] = "fail-查詢辨識記錄失敗"
    finally:
        return {
            'statusCode': 200,
            "headers": {
                "Access-Control-Allow-Headers": 'Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token',
                "Access-Control-Allow-Methods": 'GET',
                "Access-Control-Allow-Origin": '*'
            },              
            'body': json.dumps(result)
        }
  else:
  # HTTP 請求方式非 POST 回傳錯誤
    result["status"] = "fail-method error"
    return {
        'statusCode': 200,
        "headers": {
            "Access-Control-Allow-Headers": 'Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token',
            "Access-Control-Allow-Methods": 'GET',
            "Access-Control-Allow-Origin": '*'
        },          
        'body': json.dumps(result)
    }