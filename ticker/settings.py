from pydantic import BaseSettings


class Settings(BaseSettings):

    POSTGRES_HOST: str = "localhost"
    POSTGRES_PORT: int = 5432
    POSTGRES_DB: str = "trading_sample_db"
    POSTGRES_USER: str = "user"
    POSTGRES_PASSWORD: str = "very_strong_password"

    REDIS_HOST: str = "localhost"
    REDIS_PORT: int = 6379
    REDIS_DB: str = "0"

    TICKER_PERIOD: int = 5
    NUMBER_OF_TICKERS: int = 5

    class Config:
        env_file = ".env"


settings = Settings()
