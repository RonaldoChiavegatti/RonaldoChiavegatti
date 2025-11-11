from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    environment: str = "dev"
    mongo_url: str = "mongodb://mongo:27017"
    mongo_db: str = "mei_docs"
    oracle_endpoint: str
    oracle_access_key_id: str
    oracle_secret_access_key: str
    oracle_bucket: str

    class Config:
        env_file = ".env"


settings = Settings()
