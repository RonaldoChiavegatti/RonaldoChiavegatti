import uuid
from fastapi import Header, HTTPException, status


def get_current_user_id(x_user_id: str = Header(...)) -> uuid.UUID:
    """
    A dependency that extracts the user ID from the X-User-Id header.
    In a real setup, the API Gateway would be responsible for token validation
    and injecting this header.
    """
    if not x_user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User ID not found in headers",
        )
    try:
        return uuid.UUID(x_user_id)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid User ID format in headers",
        )
