from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    environment: str = "dev"
    database_url: str = "postgresql+psycopg2://appuser:apppass@postgres:5432/appdb"

    class Config:
        env_file = ".env"


settings = Settings()
