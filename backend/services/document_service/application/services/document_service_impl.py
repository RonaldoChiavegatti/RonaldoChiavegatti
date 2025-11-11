import uuid
from typing import IO, List
import pathlib

from shared.models.base_models import DocumentJob as DocumentJobResponse
from services.document_service.application.domain.document_job import DocumentJob
from services.document_service.application.ports.input.document_service import (
    DocumentService,
)
from services.document_service.application.ports.output.document_job_repository import (
    DocumentJobRepository,
)
from services.document_service.application.ports.output.file_storage import FileStorage
from services.document_service.application.ports.output.message_queue import (
    MessageQueue,
)
from services.document_service.application.exceptions import (
    JobNotFoundError,
    JobAccessForbiddenError,
)


class DocumentServiceImpl(DocumentService):
    """
    Concrete implementation of the DocumentService input port.
    """

    def __init__(
        self,
        job_repository: DocumentJobRepository,
        file_storage: FileStorage,
        message_queue: MessageQueue,
        ocr_queue_name: str = "ocr_jobs",
    ):
        self.job_repository = job_repository
        self.file_storage = file_storage
        self.message_queue = message_queue
        self.ocr_queue_name = ocr_queue_name

    def start_document_processing(
        self, user_id: uuid.UUID, file_name: str, file_content: IO[bytes]
    ) -> DocumentJobResponse:
        """
        Handles the business logic for starting a document processing job.
        1. Creates a unique path for the file.
        2. Uploads the file to storage.
        3. Creates a new DocumentJob domain entity.
        4. Saves the job to the repository.
        5. Publishes a message to the OCR queue.
        6. Returns the created job as a response DTO.
        """
        file_extension = pathlib.Path(file_name).suffix
        unique_file_name = f"{uuid.uuid4()}{file_extension}"
        storage_path = f"documents/{user_id}/{unique_file_name}"

        # 1. Upload file
        self.file_storage.upload(file_obj=file_content, destination_path=storage_path)

        # 2. Create and save job
        job = DocumentJob(user_id=user_id, file_path=storage_path)
        saved_job = self.job_repository.save(job)

        # 3. Publish message
        self.message_queue.publish_message(
            queue_name=self.ocr_queue_name,
            message={"job_id": str(saved_job.id), "file_path": saved_job.file_path},
        )

        return DocumentJobResponse.from_attributes(saved_job)

    def get_job_status(
        self, job_id: uuid.UUID, user_id: uuid.UUID
    ) -> DocumentJobResponse:
        job = self.job_repository.get_by_id(job_id)
        if not job:
            raise JobNotFoundError(f"Job with ID {job_id} not found.")

        if job.user_id != user_id:
            raise JobAccessForbiddenError("User does not have access to this job.")

        return DocumentJobResponse.from_attributes(job)

    def get_user_jobs(self, user_id: uuid.UUID) -> List[DocumentJobResponse]:
        jobs = self.job_repository.get_by_user_id(user_id)
        return [DocumentJobResponse.from_attributes(job) for job in jobs]
