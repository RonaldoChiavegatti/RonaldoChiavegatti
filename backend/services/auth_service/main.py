from fastapi import FastAPI
from services.auth_service.infrastructure.web import api
from services.auth_service.infrastructure.database import Base, engine

# This command creates the database tables if they don't exist.
# In a real production setup, you would use a migration tool like Alembic.
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Auth Service",
    description="Handles user authentication and authorization.",
    version="1.0.0",
)

app.include_router(api.router)


@app.get("/health", tags=["Health Check"])
def health_check():
    return {"status": "ok"}
