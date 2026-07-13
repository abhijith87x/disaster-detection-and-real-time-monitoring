import boto3
import os
from config import AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, AWS_REGION, AWS_BUCKET_NAME

s3 = boto3.client(
    's3',
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
    region_name=AWS_REGION
)

async def upload_file_to_s3(file):
    file.file.seek(0)
    bucket_name = AWS_BUCKET_NAME
    file_name = file.filename
    s3.upload_fileobj(file.file, bucket_name, file_name,ExtraArgs={
        "ContentType": file.content_type
    })
    return f"https://{bucket_name}.s3.{AWS_REGION}.amazonaws.com/{file_name}"

async def delete_file_from_s3(file_path):
    key = file_path.split(".amazonaws.com/")[1]
    s3.delete_object(Bucket=AWS_BUCKET_NAME, Key=key)
    return
