from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    environment: str = "dev"
    database_url: str = "postgresql+psycopg2://appuser:apppass@postgres:5432/appdb"
    jwt_secret_key: str = "troque-este-segredo"
    jwt_algorithm: str = "HS256"
    access_token_expire_minutes: int = 60

    class Config:
        env_file = ".env"


settings = Settings()
