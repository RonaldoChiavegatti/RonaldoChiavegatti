import uuid
from pydantic import BaseModel, EmailStr, Field


class User(BaseModel):
    """
    Represents the User domain entity within the auth service's bounded context.
    This model holds the core business data and is decoupled from database schemas
    or API response models.
    """

    id: uuid.UUID = Field(default_factory=uuid.uuid4)
    full_name: str
    email: EmailStr
    hashed_password: str
