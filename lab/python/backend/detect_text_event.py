import json
import boto3
import logging
from botocore.exceptions import ClientError
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)
s3_client = boto3.client("s3")
dyn_resource = boto3.resource("dynamodb")
rekognition_client = boto3.client('rekognition')
table_name = 'cfg_table'
table = dyn_resource.Table(table_name)
detect_table_name = 'detect_result_table'
detect_table = dyn_resource.Table(detect_table_name)
result = {"status":"" }

def lambda_handler(event, context):
    output_bucket = event['Records'][0]['s3']['bucket']['name']
    # s3_key_value = 'esp32-cam2s3.jpg'
    s3_key_value = event['Records'][0]['s3']['object']['key']
    # 檢驗是否需要辨識
    try:
        response = table.get_item( 
            Key={'cfg_name': 'DETECT_TEXT'},
            ConsistentRead=True,
        )
        enable_detect = False
        if response.get('Item'):
            print(response['Item'])
            enable_detect = True if response['Item']['cfg_value']==1 else False
        else:
            print('not found')
    except ClientError as err:
        logger.error(
            "檢驗是否需要辨識. Here's why: %s: %s",
            err.response["Error"]["Code"],
            err.response["Error"]["Message"],
        )  
        result["status"] = "fail-檢驗是否需要辨識"
        return {
            'statusCode': 200,
            'body': json.dumps(result)
        }    
    
    if enable_detect:
        # 辨識功能
        try:
            print(s3_key_value)
            image_content = s3_client.get_object(Bucket=output_bucket, Key=s3_key_value)['Body'].read()
            response = rekognition_client.detect_text(Image={'Bytes': image_content})
            print("共找到", len(response['TextDetections']),"筆結果")
            area,id = (0,0)
            # 找出類型為LINE且文字面積最大的結果
            for text_block in response['TextDetections']:
                if text_block['Type'] == "LINE":
                    box = text_block['Geometry']['BoundingBox']
                    text_area = box['Width'] * box['Height']
                    if text_area>area:
                        area = text_area
                        id = text_block['Id']
                        
            detected_text_result = response['TextDetections'][id]['DetectedText']
            # 寫入圖片
            datetime_format = "%Y-%m-%dT%H-%M-%S"
            taipei_time = datetime.utcnow() + timedelta(hours=8)
            timestamp_str = taipei_time.strftime(datetime_format)
            bucket_prefix = 'detected_images/'
            target_key = f'{bucket_prefix}{timestamp_str}.jpg'
            response = s3_client.put_object(
                Body = image_content,
                Bucket = output_bucket,
                Key = target_key
            )
            # 寫入資料表
            detect_table.put_item(Item={
                'date_time': timestamp_str,
                'detected_text': detected_text_result,
                'image_url': 'https://' + output_bucket + '.s3.amazonaws.com/' + target_key
            })
        except ClientError as err:
            logger.error(
                "辨識功能失敗-Here's why: %s: %s",
                err.response["Error"]["Code"],
                err.response["Error"]["Message"],
            )  
            result["status"] = "fail-辨識功能失敗"
            return {
                'statusCode': 200,
                'body': json.dumps(result)
            }    
        else:
            result["status"] = "success"
            result['result'] = detected_text_result
            

    return {
        'statusCode': 200,
        'body': json.dumps(result)
    }