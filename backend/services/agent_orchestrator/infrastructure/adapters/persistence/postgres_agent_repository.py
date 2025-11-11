import uuid
from typing import List, Optional

from services.agent_orchestrator.application.domain.agent import Agent
from services.agent_orchestrator.application.domain.knowledge import Knowledge
from services.agent_orchestrator.application.ports.output.agent_repository import (
    AgentRepository,
)
from services.agent_orchestrator.infrastructure.database import (
    AgentModel,
    KnowledgeBaseModel,
)
from sqlalchemy.orm import Session


class PostgresAgentRepository(AgentRepository):
    def __init__(self, db_session: Session):
        self.db = db_session

    def get_agent_by_id(self, agent_id: uuid.UUID) -> Optional[Agent]:
        agent_model = (
            self.db.query(AgentModel).filter(AgentModel.id == agent_id).first()
        )
        if agent_model:
            return Agent.model_validate(agent_model, from_attributes=True)
        return None

    def find_relevant_knowledge(
        self, agent_id: uuid.UUID, query: str
    ) -> List[Knowledge]:
        """
        Performs a simple case-insensitive text search on the content.
        A real implementation should use vector search on embeddings.
        """
        search_term = f"%{query}%"
        knowledge_models = (
            self.db.query(KnowledgeBaseModel)
            .filter(
                KnowledgeBaseModel.agent_id == agent_id,
                KnowledgeBaseModel.content.ilike(search_term),
            )
            .limit(5)
            .all()
        )

        return [
            Knowledge.model_validate(model, from_attributes=True)
            for model in knowledge_models
        ]
