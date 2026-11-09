
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    APP_NAME: str = "FinPilot"
    APP_VERSION: str = "1.0.0"
    DATABASE_URL: str = "postgresql+psycopg://postgres:password@localhost:5432/finpilot_db"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )


settings = Settings()
