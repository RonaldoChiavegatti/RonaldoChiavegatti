import sys
import unittest
import uuid
from datetime import datetime, timezone
from pathlib import Path

from fastapi import FastAPI
from fastapi.testclient import TestClient

# Allow imports from the project
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from services.auth_service.application.exceptions import UserNotFoundError
from services.auth_service.infrastructure.security import get_current_user_id
from services.auth_service.infrastructure.web import api
from shared.models.base_models import User as UserResponse


class FakeUserService:
    def __init__(self, user: UserResponse | None = None, raise_not_found: bool = False):
        self.user = user
        self.raise_not_found = raise_not_found

    def register_user(self, *args, **kwargs):
        raise NotImplementedError()

    def login(self, *args, **kwargs):
        raise NotImplementedError()

    def get_user_profile(self, user_id: uuid.UUID) -> UserResponse:
        if self.raise_not_found or self.user is None:
            raise UserNotFoundError("User not found")
        return self.user


class TestAuthProfileEndpoint(unittest.TestCase):
    def setUp(self):
        self.app = FastAPI()
        self.app.include_router(api.router)
        self.client = TestClient(self.app)
        self.user_id = uuid.uuid4()

    def tearDown(self):
        self.app.dependency_overrides = {}

    def test_profile_endpoint_returns_email_and_created_at(self):
        timestamp = datetime.now(timezone.utc)
        user = UserResponse(
            id=self.user_id,
            full_name="Test User",
            email="test@example.com",
            created_at=timestamp,
            updated_at=timestamp,
        )

        self.app.dependency_overrides[api.get_user_service] = lambda: FakeUserService(
            user=user
        )
        self.app.dependency_overrides[get_current_user_id] = lambda: self.user_id

        response = self.client.get("/auth/profile")

        self.assertEqual(response.status_code, 200)
        payload = response.json()
        self.assertEqual(payload["email"], "test@example.com")
        returned_timestamp = datetime.fromisoformat(
            payload["created_at"].replace("Z", "+00:00")
        )
        self.assertEqual(returned_timestamp, timestamp)

    def test_profile_endpoint_returns_404_when_user_missing(self):
        self.app.dependency_overrides[api.get_user_service] = lambda: FakeUserService(
            raise_not_found=True
        )
        self.app.dependency_overrides[get_current_user_id] = lambda: self.user_id

        response = self.client.get("/auth/profile")

        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json()["detail"], "User not found")


if __name__ == "__main__":
    unittest.main()
