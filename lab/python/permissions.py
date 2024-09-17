import boto3
import json
import pathlib

s3_client = boto3.client("s3", region_name="us-east-1")
bucket_name = "BUCKET_NAME"
current_path = str(pathlib.Path(__file__).parent.resolve())
policy_file = open(current_path + "/dataset/s3_security_policy.json", "r")

s3_client.put_bucket_policy(
    Bucket = bucket_name,
    Policy = policy_file.read()
)
