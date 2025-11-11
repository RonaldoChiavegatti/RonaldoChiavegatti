from io import BytesIO

import boto3
from botocore.client import Config

from app.core.config import settings


def get_s3_client():
    return boto3.client(
        "s3",
        endpoint_url=settings.oracle_endpoint,
        aws_access_key_id=settings.oracle_access_key_id,
        aws_secret_access_key=settings.oracle_secret_access_key,
        config=Config(signature_version="s3v4"),
    )


def download_fileobj(key: str) -> BytesIO:
    s3 = get_s3_client()
    fileobj = BytesIO()
    s3.download_fileobj(settings.oracle_bucket, key, fileobj)
    fileobj.seek(0)
    return fileobj
