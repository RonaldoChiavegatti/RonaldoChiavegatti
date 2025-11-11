from fastapi import FastAPI
from services.agent_orchestrator.infrastructure.web import api
from services.agent_orchestrator.infrastructure.database import Base, engine

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Agent Orchestrator Service",
    description="Handles AI agent chat logic, RAG, and billing integration.",
    version="1.0.0",
)

app.include_router(api.router)


@app.get("/health", tags=["Health Check"])
def health_check():
    return {"status": "ok"}
