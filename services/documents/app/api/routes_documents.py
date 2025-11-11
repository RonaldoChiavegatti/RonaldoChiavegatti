from datetime import datetime
from io import BytesIO

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile
from pymongo import MongoClient

from app.core.config import settings
from app.storage.oracle_s3 import upload_fileobj

router = APIRouter(prefix="/documents", tags=["documents"])


def get_mongo_collection():
    client = MongoClient(settings.mongo_url)
    db = client[settings.mongo_db]
    return db["documents"]


@router.get("/health")
def health_check():
    return {"status": "ok", "service": "documents"}


@router.post("/upload")
async def upload_document(file: UploadFile = File(...), collection=Depends(get_mongo_collection)):
    if file.content_type not in ["application/pdf", "image/jpeg", "image/png"]:
        raise HTTPException(status_code=400, detail="Tipo de arquivo não suportado")

    doc_key = f"{datetime.utcnow().timestamp()}_{file.filename}"
    contents = await file.read()
    upload_fileobj(fileobj=BytesIO(contents), key=doc_key)

    doc = {
        "filename": file.filename,
        "key": doc_key,
        "status": "pending",
        "created_at": datetime.utcnow(),
    }
    result = collection.insert_one(doc)

    return {"id": str(result.inserted_id), "status": "pending"}
