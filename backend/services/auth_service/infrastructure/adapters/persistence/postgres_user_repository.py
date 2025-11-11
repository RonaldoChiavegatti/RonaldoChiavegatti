from typing import Optional

from services.auth_service.application.domain.user import User as DomainUser
from services.auth_service.application.ports.output.user_repository import (
    UserRepository,
)
from services.auth_service.infrastructure.database import UserModel
from sqlalchemy.orm import Session


class PostgresUserRepository(UserRepository):
    """
    Concrete implementation of the UserRepository for PostgreSQL using SQLAlchemy.
    """

    def __init__(self, db_session: Session):
        self.db = db_session

    def get_by_email(self, email: str) -> Optional[DomainUser]:
        """
        Retrieves a user from the database by email and maps it to a domain model.
        """
        user_model = self.db.query(UserModel).filter(UserModel.email == email).first()
        if user_model:
            return DomainUser.model_validate(user_model, from_attributes=True)
        return None

    def save(self, user: DomainUser) -> DomainUser:
        """
        Saves a user domain model to the database, mapping it to a SQLAlchemy model.
        """
        # Create a new SQLAlchemy UserModel instance from the domain user data
        user_model = UserModel(
            id=user.id,
            full_name=user.full_name,
            email=user.email,
            hashed_password=user.hashed_password,
        )
        self.db.add(user_model)
        self.db.commit()
        self.db.refresh(user_model)

        # Return the saved data as a new domain user instance
        return DomainUser.model_validate(user_model, from_attributes=True)
