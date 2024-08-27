import boto3

rekognition_client = boto3.client('rekognition')
collection_id = 'Collection'

# step 4：列出集合中的面孔
maxResults=2
faces_count=0
tokens=True

response=rekognition_client.list_faces(CollectionId=collection_id,
                           MaxResults=maxResults)
print('Faces in collection ' + collection_id)
while tokens:
    faces=response['Faces']
    for face in faces:
        print (face)
        faces_count+=1
    if 'NextToken' in response:
        nextToken=response['NextToken']
        response=rekognition_client.list_faces(CollectionId=collection_id,
                               NextToken=nextToken,MaxResults=maxResults)
    else:
        tokens=False