import json
import boto3
import logging
from botocore.exceptions import ClientError

logger = logging.getLogger(__name__)
dyn_resource = boto3.resource("dynamodb")
table_name = 'cfg_table'
config_table = dyn_resource.Table(table_name)

def lambda_handler(event, context):
  result = {"status":"fail" }
  print(event['httpMethod'])
  requestMethod = event['httpMethod']
  # HTTP 請求方式為 POST 才做後續處理
  if requestMethod=='POST':
    # 設定車牌辨識選項
    try:
        print(event['body'])
        requestBody = json.loads(event['body'])
        result["status"] = "fail-參數有誤"
        if requestBody.get('enable'):
            if requestBody['enable'] in ['1','0']:
                res = config_table.update_item(
                    Key = {"cfg_name": 'DETECT_TEXT'},
                    UpdateExpression = "SET cfg_value = :v ",
                    ExpressionAttributeValues={
                        ":v": requestBody['enable']
                    },
                    ReturnValues="UPDATED_NEW"
                ) 
                result["status"] = "success"
    
    except ClientError as err:
        logger.error(
            "設定車牌辨識選項. Here's why: %s: %s",
            err.response["Error"]["Code"],
            err.response["Error"]["Message"],
        )  
        result["status"] = "fail-設定車牌辨識選項"
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
        'body': json.dumps(result)
    }