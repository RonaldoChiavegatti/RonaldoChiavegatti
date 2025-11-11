from datetime import datetime, timedelta
from typing import Dict

from jose import jwt

from services.auth_service.application.ports.output.token_provider import TokenProvider


class JwtTokenProvider(TokenProvider):
    """
    Concrete implementation of the TokenProvider port using the python-jose library.
    """

    def __init__(
        self, secret_key: str, algorithm: str, access_token_expire_minutes: int
    ):
        self.secret_key = secret_key
        self.algorithm = algorithm
        self.access_token_expire_minutes = access_token_expire_minutes

    def create_access_token(self, data: Dict) -> str:
        to_encode = data.copy()
        expire = datetime.utcnow() + timedelta(minutes=self.access_token_expire_minutes)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, self.secret_key, algorithm=self.algorithm)
        return encoded_jwt
