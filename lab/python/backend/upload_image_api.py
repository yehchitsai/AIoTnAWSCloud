import json
import boto3
import logging
from botocore.exceptions import ClientError
import base64

# 存放圖片的 S3 存儲桶 
output_bucket = 'BUCKET_NAME'
# 存放在 S3 存儲桶中的檔案名稱
s3_key_value = 'source/esp32-cam2s3.jpg'
s3_client = boto3.client('s3')
logger = logging.getLogger(__name__)
result = { "image_url":"", "status":"" }

def lambda_handler(event, context):
  requestMethod = event['httpMethod']
  # HTTP 請求方式為 POST 才做後續處理
  if requestMethod=='POST':
    # 寫入圖像
    try:
        requestBody = json.loads(event['body'])
        image_64_decode = base64.decodebytes(requestBody['key'].encode())
        response = s3_client.put_object(
            Body=image_64_decode,
            Bucket=output_bucket,
            Key=s3_key_value
        )
    except ClientError as err:
        logger.error(
            "寫入圖像失敗. Here's why: %s: %s",
            err.response["Error"]["Code"],
            err.response["Error"]["Message"],
        )  
        result["status"] = "fail-寫入圖像失敗"
        return {
            'statusCode': 200,
            'body': json.dumps(result)
        }

    result["image_url"] = 'https://' + output_bucket + '.s3.amazonaws.com/' + s3_key_value
    result["status"] = "success"
    return {
        'statusCode': 200,
        'body': json.dumps(result)
    }
  else:
  # HTTP 請求方式非 POST 回傳錯誤
    result["status"] = "fail-method error"
    return {
        'statusCode': 200,
        'body': json.dumps(result)
    }