from sqlalchemy import create_engine, Column, String, Text
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import uuid

from .config import settings

engine = create_engine(settings.DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


# SQLAlchemy Agent Table Model
class AgentModel(Base):
    __tablename__ = "agents"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, nullable=False)
    description = Column(Text)
    category = Column(String)


# SQLAlchemy KnowledgeBase Table Model
class KnowledgeBaseModel(Base):
    __tablename__ = "knowledge_base"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    agent_id = Column(UUID(as_uuid=True), index=True, nullable=False)
    title = Column(Text, nullable=False)
    content = Column(Text, nullable=False)
    embedding = Column(JSONB)  # Storing embeddings as JSONB for now


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
