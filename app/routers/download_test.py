from fastapi import FastAPI, HTTPException, APIRouter
from fastapi.responses import FileResponse
import boto3
from botocore.exceptions import NoCredentialsError
from urllib.parse import unquote
import os
from io import BytesIO

router = APIRouter()


# Configuration
SPACE_REGION = 'sgp1'
SPACES_NAME = 'jef-general-bucket'  # Replace with your region, e.g., sgp1, nyc3
ACCESS_KEY = os.getenv("SPACES_KEY")
SECRET_KEY = os.getenv("SPACES_SECRET")
ENDPOINT = os.getenv("SPACES_ENDPOINT")


# Create a session and client
session = boto3.session.Session()
client = session.client(
    "s3",
    region_name=SPACE_REGION,
    endpoint_url=f"https://{SPACE_REGION}.digitaloceanspaces.com",
    aws_access_key_id=ACCESS_KEY,
    aws_secret_access_key=SECRET_KEY,
)



# Function to download a file from DigitalOcean Spaces using `download_fileobj`
def download_file_from_space(bucket_name, object_name):
    try:
        # Use a file-like object to download the file
        file_obj = BytesIO()
        client.download_fileobj(bucket_name, object_name, file_obj)
        file_obj.seek(0)  # Rewind the file-like object to the beginning
        return file_obj
    except NoCredentialsError:
        raise HTTPException(status_code=403, detail="Credentials not available")
    except Exception as e:
        raise HTTPException(status_code=404, detail=f"An error occurred: {e}")

#Test Route to Download a file from DigitalOcean Spaces
@router.get("/test-download")
async def download_test():
    bucket_name = SPACES_NAME
    object_name = 'uploaded-files/p1.jpg'
    file_obj = download_file_from_space(bucket_name, object_name)
    return FileResponse(file_obj, media_type='application/octet-stream', filename='FILE_NAME')