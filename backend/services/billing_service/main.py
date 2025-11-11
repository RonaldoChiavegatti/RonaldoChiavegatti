from fastapi import FastAPI
from services.billing_service.infrastructure.web import api
from services.billing_service.infrastructure.database import Base, engine

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Billing Service",
    description="Handles user token balances and transactions.",
    version="1.0.0",
)

app.include_router(api.router)


@app.get("/health", tags=["Health Check"])
def health_check():
    return {"status": "ok"}
