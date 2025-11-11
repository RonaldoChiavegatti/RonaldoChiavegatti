from io import BytesIO

from pymongo import MongoClient

from app.celery_app import celery_app
from app.core.config import settings
from app.storage.oracle_s3 import get_s3_client


@celery_app.task
def process_document(document_id: str):
    """Processa documentos enviados, executando OCR e enriquecimento."""
    print(f"[Worker] Processando documento {document_id}")

    mongo_client = MongoClient(settings.mongo_url)
    documents = mongo_client[settings.mongo_db]["documents"]
    documents.update_one({"_id": document_id}, {"$set": {"status": "processing"}}, upsert=True)

    s3 = get_s3_client()
    buffer = BytesIO()
    # TODO: baixar arquivo real e processar OCR
    print(f"[Worker] Placeholder para baixar {document_id} usando {s3} e buffer {buffer}")
