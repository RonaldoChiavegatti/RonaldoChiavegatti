from abc import ABC, abstractmethod
from pydantic import EmailStr

from shared.models.base_models import User as UserResponse, Token


class UserService(ABC):
    """Input port defining the user service use cases."""

    @abstractmethod
    def register_user(
        self, full_name: str, email: EmailStr, password: str
    ) -> UserResponse:
        """
        Use case for registering a new user.
        """
        pass

    @abstractmethod
    def login(self, email: EmailStr, password: str) -> Token:
        """
        Use case for user login. Returns an access token on success.
        """
        pass
