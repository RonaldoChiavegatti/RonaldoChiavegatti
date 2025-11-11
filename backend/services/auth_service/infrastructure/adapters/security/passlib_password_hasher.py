from passlib.context import CryptContext

from services.auth_service.application.ports.output.password_hasher import (
    PasswordHasher,
)


class PasslibPasswordHasher(PasswordHasher):
    """
    Concrete implementation of the PasswordHasher port using the passlib library.
    """

    def __init__(self):
        self.pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    def hash(self, plain_password: str) -> str:
        return self.pwd_context.hash(plain_password)

    def verify(self, plain_password: str, hashed_password: str) -> bool:
        return self.pwd_context.verify(plain_password, hashed_password)
