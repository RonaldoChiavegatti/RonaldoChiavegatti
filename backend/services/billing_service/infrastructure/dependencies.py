from fastapi import Depends
from sqlalchemy.orm import Session

from services.billing_service.infrastructure.database import get_db
from services.billing_service.application.ports.input.billing_service import (
    BillingService,
)
from services.billing_service.application.services.billing_service_impl import (
    BillingServiceImpl,
)
from services.billing_service.infrastructure.adapters.persistence.postgres_billing_repository import (
    PostgresBillingRepository,
)


def get_billing_service(db: Session = Depends(get_db)) -> BillingService:
    """
    Composition Root for the BillingService.
    """
    billing_repo = PostgresBillingRepository(db)
    return BillingServiceImpl(billing_repository=billing_repo)
