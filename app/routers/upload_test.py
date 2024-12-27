from fastapi import APIRouter, File, UploadFile
import boto3
from botocore.exceptions import NoCredentialsError, PartialCredentialsError

import os 

router = APIRouter()


# Configuration
SPACE_REGION = 'sgp1'
SPACES_NAME = 'jef-general-bucket'  # Replace with your region, e.g., sgp1, nyc3
ACCESS_KEY = os.getenv("SPACES_KEY")
SECRET_KEY = os.getenv("SPACES_SECRET")
ENDPOINT = os.getenv("SPACES_ENDPOINT")


# Create a session and client
session = boto3.session.Session()
s3_client = session.client(
    "s3",
    region_name=SPACE_REGION,
    endpoint_url=f"https://{SPACE_REGION}.digitaloceanspaces.com",
    aws_access_key_id=ACCESS_KEY,
    aws_secret_access_key=SECRET_KEY,
)

@router.post("/uploadfile/")
async def upload_file_to_spaces(file: UploadFile):
    try:
        # Upload file to DigitalOcean Spaces
        key = f"uploaded-files/{file.filename}"
        s3_client.upload_fileobj(file.file, SPACES_NAME, key)

        return {
            "filename": file.filename,
            "status": "uploaded",
            "location": f"https://{SPACES_NAME}.{SPACE_REGION}.digitaloceanspaces.com/{key}",
        }
    except (NoCredentialsError, PartialCredentialsError):
        return {"error": "Invalid DigitalOcean Spaces credentials"}
    except Exception as e:
        return {"error": str(e)}