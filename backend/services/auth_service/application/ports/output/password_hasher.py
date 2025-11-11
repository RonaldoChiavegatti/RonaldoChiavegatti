from abc import ABC, abstractmethod


class PasswordHasher(ABC):
    """Output port for handling password hashing and verification."""

    @abstractmethod
    def hash(self, plain_password: str) -> str:
        """Hashes a plain text password."""
        pass

    @abstractmethod
    def verify(self, plain_password: str, hashed_password: str) -> bool:
        """Verifies a plain password against a hashed one."""
        pass
