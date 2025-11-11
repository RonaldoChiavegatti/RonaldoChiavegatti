import binascii
import hashlib
import hmac
import secrets

from services.auth_service.application.ports.output.password_hasher import (
    PasswordHasher,
)


class PBKDF2PasswordHasher(PasswordHasher):
    """
    Password hasher built on the Python stdlib (hashlib.pbkdf2_hmac).
    Stores hashes in the format: pbkdf2_sha256$iterations$salt$hash.
    """

    algorithm = "pbkdf2_sha256"
    iterations = 390000  # mirrors Django 4.x default
    salt_size = 16  # bytes

    def hash(self, plain_password: str) -> str:
        salt = secrets.token_bytes(self.salt_size)
        dk = hashlib.pbkdf2_hmac(
            "sha256", plain_password.encode("utf-8"), salt, self.iterations
        )
        return self._encode(salt, dk)

    def verify(self, plain_password: str, hashed_password: str) -> bool:
        algorithm, iterations, salt_hex, hash_hex = self._decode(hashed_password)
        if algorithm != self.algorithm:
            return False

        salt = binascii.unhexlify(salt_hex)
        expected_hash = binascii.unhexlify(hash_hex)
        new_hash = hashlib.pbkdf2_hmac(
            "sha256",
            plain_password.encode("utf-8"),
            salt,
            int(iterations),
        )
        return hmac.compare_digest(new_hash, expected_hash)

    def _encode(self, salt: bytes, derived_key: bytes) -> str:
        return f"{self.algorithm}${self.iterations}${salt.hex()}${derived_key.hex()}"

    def _decode(self, encoded: str):
        try:
            algorithm, iterations, salt_hex, hash_hex = encoded.split("$")
        except ValueError:
            raise ValueError("Invalid hashed password format")
        return algorithm, iterations, salt_hex, hash_hex
