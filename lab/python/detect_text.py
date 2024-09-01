import boto3, json
from io import BytesIO

rekognition_client = boto3.client('rekognition')
s3_client = boto3.client('s3')

bucket_name = "aiotnawscloud0821"
bucket_prefix = 'images/'
target_image = "yehchitsai.jpg"

image_content = s3_client.get_object(Bucket=bucket_name, Key=bucket_prefix + target_image)['Body'].read()

response = rekognition_client.detect_text(Image={'Bytes': image_content})
print("共找到", len(response['TextDetections']),"筆結果")
area = 0
id = 0
# 找出類型為LINE且文字面積最大的結果
for text_block in response['TextDetections']:
    print("第",(text_block['Id']+1),'筆文字為：',text_block['DetectedText'],'，類型為：',text_block['Type'])
    if text_block['Type'] == "LINE":
        box = text_block['Geometry']['BoundingBox']
        text_area = box['Width'] * box['Height']
        if text_area>area:
            area = text_area
            id = text_block['Id']

print("\n類型為 LINE 且文字面積最大的結果為：",response['TextDetections'][id]['DetectedText'])
