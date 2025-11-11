import uuid
from datetime import datetime
from pydantic import BaseModel


class UserBalance(BaseModel):
    user_id: uuid.UUID
    balance: int
    last_updated_at: datetime
