from fastapi import Depends
from services.auth_service.application.ports.input.user_service import UserService
from services.auth_service.application.services.user_service_impl import UserServiceImpl
from services.auth_service.infrastructure.adapters.persistence.postgres_user_repository import (
    PostgresUserRepository,
)
from services.auth_service.infrastructure.adapters.security.jwt_token_provider import (
    JwtTokenProvider,
)
from services.auth_service.infrastructure.adapters.security.pbkdf2_password_hasher import (
    PBKDF2PasswordHasher,
)
from services.auth_service.infrastructure.config import settings
from services.auth_service.infrastructure.database import get_db
from sqlalchemy.orm import Session


def get_user_service(db: Session = Depends(get_db)) -> UserService:
    """
    This is the Composition Root for the UserService.
    It instantiates all adapters and injects them into the service.
    FastAPI will cache the result for a single request.
    """
    user_repo = PostgresUserRepository(db)
    password_hasher = PBKDF2PasswordHasher()
    token_provider = JwtTokenProvider(
        secret_key=settings.SECRET_KEY,
        algorithm=settings.ALGORITHM,
        access_token_expire_minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES,
    )
    return UserServiceImpl(
        user_repository=user_repo,
        password_hasher=password_hasher,
        token_provider=token_provider,
    )
