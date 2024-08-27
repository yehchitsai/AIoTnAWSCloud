import boto3
import botocore

rekognition_client = boto3.client('rekognition')
# step 7. 刪除集合
collection_id = 'Collection'
print('Attempting to delete collection ' + collection_id)
status_code=0
try:
    response=rekognition_client.delete_collection(CollectionId=collection_id)
    status_code=response['StatusCode']
    print('All done!')
    print(status_code)
    
except botocore.exceptions.ClientError as e:
    if e.response['Error']['Code'] == 'ResourceNotFoundException':
        print ('The collection ' + collection_id + ' was not found ')
    else:
        print ('Error other than Not Found occurred: ' + e.response['Error']['Message'])
    status_code=e.response['ResponseMetadata']['HTTPStatusCode']