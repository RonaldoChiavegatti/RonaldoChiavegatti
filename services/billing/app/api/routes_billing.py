from fastapi import APIRouter

router = APIRouter(prefix="/billing", tags=["billing"])


@router.get("/health")
def health_check():
    return {"status": "ok", "service": "billing"}


@router.get("/summary")
def get_usage_summary():
    return {
        "month": "2025-11",
        "total_tokens": 0,
        "total_requests": 0,
    }
