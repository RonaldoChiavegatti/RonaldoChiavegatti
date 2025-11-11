from abc import ABC, abstractmethod
from typing import List, Optional
import uuid

from services.billing_service.application.domain.transaction import Transaction
from services.billing_service.application.domain.balance import UserBalance


class BillingRepository(ABC):
    """Output port for billing persistence."""

    @abstractmethod
    def get_user_balance(self, user_id: uuid.UUID) -> Optional[UserBalance]:
        """Fetches a user's balance by their ID."""
        pass

    @abstractmethod
    def get_user_transactions(self, user_id: uuid.UUID) -> List[Transaction]:
        """Fetches all transactions for a given user."""
        pass

    @abstractmethod
    def create_transaction_and_update_balance(
        self, transaction: Transaction
    ) -> (UserBalance, Transaction):
        """
        Saves a new transaction and updates the user's balance accordingly in a single atomic operation.
        Returns the updated balance and the created transaction.
        """
        pass
