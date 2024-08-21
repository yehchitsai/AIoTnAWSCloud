import boto3
import json

s3_client = boto3.client("s3", region_name="us-east-1")
bucket_name = "<bucket-name>"

policy_file = open("s3_security_policy.json", "r")


s3_client.put_bucket_policy(
    Bucket = bucket_name,
    Policy = policy_file.read()
)
