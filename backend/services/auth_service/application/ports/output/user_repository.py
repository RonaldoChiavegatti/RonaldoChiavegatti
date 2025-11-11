from abc import ABC, abstractmethod
from typing import Optional
import uuid

from services.auth_service.application.domain.user import User


class UserRepository(ABC):
    """Output port for user persistence."""

    @abstractmethod
    def get_by_email(self, email: str) -> Optional[User]:
        """Fetches a user by their email from the persistence layer."""
        pass

    @abstractmethod
    def save(self, user: User) -> User:
        """Saves a new or updated user to the persistence layer."""
        pass
