import uuid
import httpx

from services.agent_orchestrator.application.ports.output.billing_service import (
    BillingService,
)


class HttpBillingService(BillingService):
    def __init__(self, base_url: str):
        self.base_url = base_url

    def charge_tokens(self, user_id: uuid.UUID, amount: int, description: str) -> bool:
        """
        Makes an HTTP POST request to the external billing service.
        """
        payload = {
            "user_id": str(user_id),
            "amount": amount,
            "description": description,
        }

        try:
            with httpx.Client() as client:
                response = client.post(
                    f"{self.base_url}/billing/charge-tokens", json=payload
                )
                return response.status_code == 200
        except httpx.RequestError:
            return False
