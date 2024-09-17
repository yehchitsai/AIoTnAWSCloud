import boto3
from io import BytesIO
from PIL import Image, ImageDraw


rekognition_client = boto3.client('rekognition')
s3_client = boto3.client('s3')

bucket_name = "BUCKET_NAME"
bucket_prefix = 'images/'
one_person_image = "target.jpg"
one_person_image_box = "target-box.jpg"

#step 1. 創建集合 
collection_id = 'Collection'
response = rekognition_client.create_collection(CollectionId=collection_id)
print('Collection ARN: ' + response['CollectionArn'])

# step 2. 將圖像添加到集合
image_content = s3_client.get_object(Bucket=bucket_name, Key=bucket_prefix + one_person_image)['Body'].read()

response = rekognition_client.index_faces(CollectionId = collection_id,
                         Image={'Bytes': image_content},
                         ExternalImageId=one_person_image,
                         MaxFaces=1,
                         QualityFilter="AUTO",
                         DetectionAttributes=['ALL'])

# step 3. 查看為圖像創建的邊界框
img = Image.open(BytesIO(image_content))
imgWidth, imgHeight = img.size
draw = ImageDraw.Draw(img)

for faceRecord in response['FaceRecords']:
    print('  Face ID: ' + faceRecord['Face']['FaceId'])
    print('  Location: {}'.format(faceRecord['Face']['BoundingBox']))    
    box = faceRecord['Face']['BoundingBox']
    left = imgWidth * box['Left']
    top = imgHeight * box['Top']
    width = imgWidth * box['Width']
    height = imgHeight * box['Height']

    points = ((left,top),(left+width,top),(left+width,top+height),(left,top+height),(left,top))

    draw.line(points,fill='#00d400', width=15)
    
    img_bytes = BytesIO()
    img.save(img_bytes, format='JPEG')
    img_bytes = img_bytes.getvalue()
    # Upload the modified image back to S3
    s3_client.put_object(Bucket=bucket_name, Key=bucket_prefix + one_person_image_box, Body=img_bytes)