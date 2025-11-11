from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DATABASE_URL: str
    GEMINI_API_KEY: str
    BILLING_SERVICE_URL: str  # e.g., http://billing-service:8004

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()
