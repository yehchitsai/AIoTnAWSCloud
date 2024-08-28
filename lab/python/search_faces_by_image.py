import boto3
import json
from io import BytesIO
from PIL import Image, ImageDraw

rekognition_client = boto3.client('rekognition')
s3_client = boto3.client('s3')

bucket_name = "aiotnawscloud0821"
bucket_prefix = 'images/'
people_image = 'group.jpg'
people_image_box = 'group-box.jpg'
collection_id = 'Collection'
# step 5：使用集合找到面孔
threshold = 10
maxFaces=2

image_content = s3_client.get_object(Bucket=bucket_name, Key=bucket_prefix + people_image)['Body'].read()
response2=rekognition_client.search_faces_by_image(CollectionId=collection_id,
                        Image={'Bytes': image_content},
                        FaceMatchThreshold=threshold,
                        MaxFaces=maxFaces)

print(json.dumps(response2,default=str))
faceMatches=response2['FaceMatches']
print ('Matching faces', len(faceMatches))
for match in faceMatches:
    print(json.dumps(match,default=str))
    print ('FaceId:' + match['Face']['FaceId'])
    print ('Similarity: ' + "{:.2f}".format(match['Similarity']) + "%")
    print ('ExternalImageId: ' + match['Face']['ExternalImageId'])
    # step 6：查看找到的面孔的邊界框
    targetimage = Image.open(BytesIO(image_content))
    imgWidth, imgHeight = targetimage.size
    
    draw = ImageDraw.Draw(targetimage)
    # box = match['Face']['BoundingBox']
    box = response2['SearchedFaceBoundingBox']

    left = imgWidth * box['Left']
    top = imgHeight * box['Top']
    width = imgWidth * box['Width']
    height = imgHeight * box['Height']
    
    points = ((left,top),(left+width,top),(left+width,top+height),(left,top+height),(left,top))
    draw.line(points,fill='#00d400', width=15)
    
    img_bytes = BytesIO()
    targetimage.save(img_bytes, format='JPEG')
    img_bytes = img_bytes.getvalue()
    # Upload the modified image back to S3
    s3_client.put_object(Bucket=bucket_name, Key=bucket_prefix + people_image_box, Body=img_bytes)