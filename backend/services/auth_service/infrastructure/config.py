from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """
    Manages service configuration using environment variables.
    """

    DATABASE_URL: str
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    class Config:
        # In a real scenario, you would have a .env file in the root
        # or pass environment variables to the Docker container.
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()
