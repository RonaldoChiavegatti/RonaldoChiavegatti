import unittest
from unittest.mock import MagicMock
import uuid

import sys
from pathlib import Path

project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from services.agent_orchestrator.application.services.orchestrator_service_impl import (
    OrchestratorServiceImpl,
)
from services.agent_orchestrator.application.domain.agent import Agent
from services.agent_orchestrator.application.domain.knowledge import Knowledge
from services.agent_orchestrator.application.exceptions import (
    AgentNotFoundError,
    InsufficientBalanceError,
)
from services.agent_orchestrator.application.ports.output.agent_repository import (
    AgentRepository,
)
from services.agent_orchestrator.application.ports.output.llm_provider import (
    LLMProvider,
)
from services.agent_orchestrator.application.ports.output.billing_service import (
    BillingService,
)


class TestOrchestratorService(unittest.TestCase):
    def setUp(self):
        self.mock_agent_repo = MagicMock(spec=AgentRepository)
        self.mock_llm_provider = MagicMock(spec=LLMProvider)
        self.mock_billing_service = MagicMock(spec=BillingService)

        self.service = OrchestratorServiceImpl(
            agent_repository=self.mock_agent_repo,
            llm_provider=self.mock_llm_provider,
            billing_service=self.mock_billing_service,
        )

        self.user_id = uuid.uuid4()
        self.agent_id = uuid.uuid4()
        self.test_agent = Agent(id=self.agent_id, name="Test Agent")
        self.test_knowledge = Knowledge(
            id=uuid.uuid4(), title="Test", content="This is a test."
        )

    def test_handle_chat_message_success(self):
        # Arrange
        self.mock_agent_repo.get_agent_by_id.return_value = self.test_agent
        self.mock_agent_repo.find_relevant_knowledge.return_value = [
            self.test_knowledge
        ]
        self.mock_llm_provider.generate_response.return_value = (
            "This is the LLM response."
        )
        self.mock_billing_service.charge_tokens.return_value = True

        # Act
        response = self.service.handle_chat_message(
            user_id=self.user_id,
            agent_id=self.agent_id,
            user_message="Hello",
            conversation_history=[],
        )

        # Assert
        self.mock_agent_repo.get_agent_by_id.assert_called_once_with(self.agent_id)
        self.mock_agent_repo.find_relevant_knowledge.assert_called_once_with(
            agent_id=self.agent_id, query="Hello"
        )
        self.mock_llm_provider.generate_response.assert_called_once()
        self.mock_billing_service.charge_tokens.assert_called_once()
        self.assertEqual(response, "This is the LLM response.")

    def test_handle_chat_message_agent_not_found(self):
        # Arrange
        self.mock_agent_repo.get_agent_by_id.return_value = None

        # Act & Assert
        with self.assertRaises(AgentNotFoundError):
            self.service.handle_chat_message(
                user_id=self.user_id,
                agent_id=self.agent_id,
                user_message="Hello",
                conversation_history=[],
            )
        self.mock_llm_provider.generate_response.assert_not_called()
        self.mock_billing_service.charge_tokens.assert_not_called()

    def test_handle_chat_message_insufficient_balance(self):
        # Arrange
        self.mock_agent_repo.get_agent_by_id.return_value = self.test_agent
        self.mock_agent_repo.find_relevant_knowledge.return_value = [
            self.test_knowledge
        ]
        self.mock_llm_provider.generate_response.return_value = (
            "This is the LLM response."
        )
        self.mock_billing_service.charge_tokens.return_value = False

        # Act & Assert
        with self.assertRaises(InsufficientBalanceError):
            self.service.handle_chat_message(
                user_id=self.user_id,
                agent_id=self.agent_id,
                user_message="Hello",
                conversation_history=[],
            )

        self.mock_llm_provider.generate_response.assert_called_once()
        self.mock_billing_service.charge_tokens.assert_called_once()


if __name__ == "__main__":
    unittest.main()
