from abc import ABC, abstractmethod
import uuid


class BillingService(ABC):
    """
    Output port for communicating with the billing service.
    This is an adapter to another internal service.
    """

    @abstractmethod
    def charge_tokens(self, user_id: uuid.UUID, amount: int, description: str) -> bool:
        """
        Charges a user for a certain amount of tokens.
        Returns True on success, False on failure.
        """
        pass
