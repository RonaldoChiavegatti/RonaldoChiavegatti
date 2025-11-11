from abc import ABC, abstractmethod
from typing import List
import uuid

from services.agent_orchestrator.application.domain.message import Message


class OrchestratorService(ABC):
    """Input port defining the chat orchestration use cases."""

    @abstractmethod
    def handle_chat_message(
        self,
        user_id: uuid.UUID,
        agent_id: uuid.UUID,
        user_message: str,
        conversation_history: List[Message],
    ) -> str:
        """
        Handles a new user message in a conversation.
        - Retrieves relevant knowledge.
        - Constructs a prompt for the LLM.
        - Generates a response.
        - Charges the user for token usage.
        Returns the assistant's response message.
        """
        pass
