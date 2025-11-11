import uuid
from typing import Optional
from pydantic import BaseModel


class Agent(BaseModel):
    id: uuid.UUID
    name: str
    description: Optional[str] = None
    category: Optional[str] = None
