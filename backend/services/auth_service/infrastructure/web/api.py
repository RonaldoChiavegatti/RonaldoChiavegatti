from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from shared.models.base_models import User as UserResponse, Token, UserCreate
from services.auth_service.application.ports.input.user_service import UserService
from services.auth_service.application.exceptions import (
    UserAlreadyExistsError,
    InvalidCredentialsError,
)
from services.auth_service.infrastructure.dependencies import get_user_service

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post(
    "/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED
)
def register_user_endpoint(
    user_create: UserCreate, user_service: UserService = Depends(get_user_service)
):
    try:
        user = user_service.register_user(
            full_name=user_create.full_name,
            email=user_create.email,
            password=user_create.password,
        )
        return user
    except UserAlreadyExistsError as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error",
        )


@router.post("/login", response_model=Token)
def login_for_access_token_endpoint(
    form_data: OAuth2PasswordRequestForm = Depends(),
    user_service: UserService = Depends(get_user_service),
):
    try:
        # OAuth2 uses 'username' field for the email
        token = user_service.login(
            email=form_data.username, password=form_data.password
        )
        return token
    except InvalidCredentialsError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(e),
            headers={"WWW-Authenticate": "Bearer"},
        )
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error",
        )
