from abc import ABC, abstractmethod
from typing import Dict, Any


class MessageQueue(ABC):
    """Output port for publishing messages to a queue."""

    @abstractmethod
    def publish_message(self, queue_name: str, message: Dict[str, Any]):
        """Publishes a message to the specified queue."""
        pass
