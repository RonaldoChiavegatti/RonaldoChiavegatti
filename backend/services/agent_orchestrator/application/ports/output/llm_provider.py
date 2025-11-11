from abc import ABC, abstractmethod
from typing import List

from services.agent_orchestrator.application.domain.message import Message


class LLMProvider(ABC):
    """Output port for interacting with a Large Language Model."""

    @abstractmethod
    def generate_response(self, messages: List[Message]) -> str:
        """
        Generates a response from the LLM based on a list of messages (conversation history).
        """
        pass
