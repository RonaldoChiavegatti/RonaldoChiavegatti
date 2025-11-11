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


def upload_fileobj(fileobj, key: str):
    s3 = get_s3_client()
    s3.upload_fileobj(fileobj, settings.oracle_bucket, key)


def generate_presigned_url(key: str, expires_in: int = 3600) -> str:
    s3 = get_s3_client()
    return s3.generate_presigned_url(
        "get_object",
        Params={"Bucket": settings.oracle_bucket, "Key": key},
        ExpiresIn=expires_in,
    )
