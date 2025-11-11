from abc import ABC, abstractmethod
from typing import Dict


class TokenProvider(ABC):
    """Output port for JWT token creation and verification."""

    @abstractmethod
    def create_access_token(self, data: Dict) -> str:
        """Creates a new JWT access token."""
        pass
