import uuid
from pydantic import BaseModel


class Knowledge(BaseModel):
    id: uuid.UUID
    title: str
    content: str
