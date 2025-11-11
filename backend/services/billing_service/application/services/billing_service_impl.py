import uuid
from datetime import datetime
from typing import List

from services.billing_service.application.domain.transaction import (
    Transaction,
    TransactionType,
)
from services.billing_service.application.exceptions import UserNotFoundError
from services.billing_service.application.ports.input.billing_service import (
    BillingService,
)
from services.billing_service.application.ports.output.billing_repository import (
    BillingRepository,
)
from shared.models.base_models import (
    Transaction as TransactionResponse,
)
from shared.models.base_models import (
    UserBalance as UserBalanceResponse,
)


class BillingServiceImpl(BillingService):
    """
    Concrete implementation of the BillingService input port.
    """

    def __init__(self, billing_repository: BillingRepository):
        self.billing_repository = billing_repository

    def charge_user(self, user_id: uuid.UUID, amount: int, description: str) -> bool:
        current_balance = self.billing_repository.get_user_balance(user_id)

        if not current_balance or current_balance.balance < amount:
            return False

        transaction = Transaction(
            id=uuid.uuid4(),
            user_id=user_id,
            amount=-amount,  # Charging deducts from the balance
            type=TransactionType.CHARGE,
            description=description,
            created_at=datetime.utcnow(),
        )

        try:
            self.billing_repository.create_transaction_and_update_balance(transaction)
            return True
        except Exception:
            return False

    def get_user_balance(self, user_id: uuid.UUID) -> UserBalanceResponse:
        balance = self.billing_repository.get_user_balance(user_id)
        if not balance:
            raise UserNotFoundError(f"Balance for user ID {user_id} not found.")

        return UserBalanceResponse.model_validate(balance, from_attributes=True)

    def get_user_transactions(self, user_id: uuid.UUID) -> List[TransactionResponse]:
        transactions = self.billing_repository.get_user_transactions(user_id)
        return [
            TransactionResponse.model_validate(tx, from_attributes=True)
            for tx in transactions
        ]
