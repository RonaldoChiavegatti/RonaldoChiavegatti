from abc import ABC, abstractmethod
from typing import List, Optional
import uuid

from services.agent_orchestrator.application.domain.agent import Agent
from services.agent_orchestrator.application.domain.knowledge import Knowledge


class AgentRepository(ABC):
    """Output port for agent and knowledge persistence."""

    @abstractmethod
    def get_agent_by_id(self, agent_id: uuid.UUID) -> Optional[Agent]:
        """Fetches an agent by its ID."""
        pass

    @abstractmethod
    def find_relevant_knowledge(
        self, agent_id: uuid.UUID, query: str
    ) -> List[Knowledge]:
        """
        Finds knowledge base articles relevant to a query for a specific agent.
        This would typically involve a vector search on embeddings.
        """
        pass
