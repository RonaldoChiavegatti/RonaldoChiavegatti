from typing import IO
from minio import Minio
from minio.error import S3Error

from services.document_service.application.ports.output.file_storage import FileStorage


class MinioFileStorage(FileStorage):
    def __init__(
        self,
        endpoint: str,
        access_key: str,
        secret_key: str,
        bucket_name: str,
        secure: bool = False,
    ):
        self.client = Minio(
            endpoint, access_key=access_key, secret_key=secret_key, secure=secure
        )
        self.bucket_name = bucket_name
        self._ensure_bucket_exists()

    def _ensure_bucket_exists(self):
        found = self.client.bucket_exists(self.bucket_name)
        if not found:
            self.client.make_bucket(self.bucket_name)

    def upload(self, file_obj: IO[bytes], destination_path: str) -> str:
        file_obj.seek(0, 2)
        file_size = file_obj.tell()
        file_obj.seek(0)

        try:
            self.client.put_object(
                bucket_name=self.bucket_name,
                object_name=destination_path,
                data=file_obj,
                length=file_size,
            )
            return destination_path
        except S3Error as exc:
            raise IOError(f"Failed to upload to MinIO: {exc}")
