from fastapi import FastAPI, HTTPException, APIRouter
import boto3
from botocore.exceptions import NoCredentialsError, ClientError
import os
import logging
import requests

router = APIRouter()

# Configuration
SPACE_REGION = 'sgp1'
SPACES_NAME = 'jef-general-bucket'  # Replace with your actual bucket name
ACCESS_KEY = os.getenv("SPACES_KEY")
SECRET_KEY = os.getenv("SPACES_SECRET")
ENDPOINT = os.getenv("SPACES_ENDPOINT")

# Initialize S3 client with custom credentials and endpoint
def get_s3_client():
    return boto3.client(
        's3',
        aws_access_key_id=ACCESS_KEY,
        aws_secret_access_key=SECRET_KEY,
        endpoint_url=f'https://{SPACE_REGION}.digitaloceanspaces.com'  # Correct endpoint
    )


@router.get("/test-download")
def create_presigned_url(bucket_name: str, object_name: str, expiration: int = 3600):
    """Generate a presigned URL to share an S3 object

    :param bucket_name: string
    :param object_name: string
    :param expiration: Time in seconds for the presigned URL to remain valid
    :return: Presigned URL as string. If error, returns None.
    """
    s3_client = get_s3_client()

    try:
        response = s3_client.generate_presigned_url('get_object',
                                                    Params={'Bucket': bucket_name,
                                                            'Key': object_name},
                                                    ExpiresIn=expiration)
    except ClientError as e:
        logging.error(f"Error generating presigned URL: {e}")
        raise HTTPException(status_code=500, detail="Error generating presigned URL")
    
    # The response contains the presigned URL
    return {"url": response}

# Example call to the FastAPI endpoint
# The URL is expected to be called with bucket_name and object_name as query params
# For example: GET /test-download?bucket_name=jef-general-bucket&object_name=uploaded-files/p1.jpg
