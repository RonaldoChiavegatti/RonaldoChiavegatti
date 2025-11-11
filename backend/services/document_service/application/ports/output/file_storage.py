from abc import ABC, abstractmethod
from typing import IO


class FileStorage(ABC):
    """Output port for handling file storage operations."""

    @abstractmethod
    def upload(self, file_obj: IO[bytes], destination_path: str) -> str:
        """
        Uploads a file-like object to the storage.
        Returns the public URL or path of the uploaded file.
        """
        pass
