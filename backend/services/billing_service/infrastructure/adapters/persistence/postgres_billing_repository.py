from typing import List, Optional
import uuid
from sqlalchemy.orm import Session
from sqlalchemy import desc

from services.billing_service.application.ports.output.billing_repository import (
    BillingRepository,
)
from services.billing_service.application.domain.transaction import Transaction
from services.billing_service.application.domain.balance import UserBalance
from services.billing_service.infrastructure.database import (
    UserBalanceModel,
    TransactionModel,
)


class PostgresBillingRepository(BillingRepository):
    def __init__(self, db_session: Session):
        self.db = db_session

    def get_user_balance(self, user_id: uuid.UUID) -> Optional[UserBalance]:
        balance_model = (
            self.db.query(UserBalanceModel)
            .filter(UserBalanceModel.user_id == user_id)
            .first()
        )
        if balance_model:
            return UserBalance.from_attributes(balance_model)
        return None

    def get_user_transactions(self, user_id: uuid.UUID) -> List[Transaction]:
        transaction_models = (
            self.db.query(TransactionModel)
            .filter(TransactionModel.user_id == user_id)
            .order_by(desc(TransactionModel.created_at))
            .all()
        )
        return [Transaction.from_attributes(model) for model in transaction_models]

    def create_transaction_and_update_balance(
        self, transaction: Transaction
    ) -> (UserBalance, Transaction):
        try:
            # Lock the user's balance row to prevent race conditions
            balance_model = (
                self.db.query(UserBalanceModel)
                .filter(UserBalanceModel.user_id == transaction.user_id)
                .with_for_update()
                .one()
            )

            # Update the balance
            balance_model.balance += transaction.amount

            # Create the new transaction
            transaction_model = TransactionModel(**transaction.model_dump())

            self.db.add(transaction_model)
            self.db.commit()

            self.db.refresh(balance_model)
            self.db.refresh(transaction_model)

            updated_balance = UserBalance.from_attributes(balance_model)
            created_transaction = Transaction.from_attributes(transaction_model)

            return updated_balance, created_transaction

        except Exception as e:
            self.db.rollback()
            raise e
