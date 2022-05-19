from pydantic import BaseSettings


class Settings(BaseSettings):
    WEB_SERVICE_PORT: int = 8000

    POSTGRES_HOST: str = "localhost"
    POSTGRES_PORT: int = 5432
    POSTGRES_DB: str = "trading_sample_db"
    POSTGRES_USER: str = "user"
    POSTGRES_PASSWORD: str = "very_strong_password"

    REDIS_HOST: str = "localhost"
    REDIS_PORT: int = 6379
    REDIS_DB: str = "0"

    class Config:
        env_file = ".env"


settings = Settings()
