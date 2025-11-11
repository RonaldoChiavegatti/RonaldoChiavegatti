from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.auth import Token, UserCreate, UserLogin

router = APIRouter(prefix="/auth", tags=["auth"])


@router.get("/health")
def health_check():
    return {"status": "ok", "service": "auth"}


@router.post("/register", response_model=dict)
def register_user(payload: UserCreate, db: Session = Depends(get_db)):
    return {"message": "register endpoint - implementar lógica"}


@router.post("/login", response_model=Token)
def login(payload: UserLogin, db: Session = Depends(get_db)):
    fake_token = "IMPLEMENTAR_JWT_AQUI"
    return Token(access_token=fake_token)
