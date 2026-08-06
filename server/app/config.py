import os
from pydantic_settings import BaseSettings, SettingsConfigDict

THEME_OPTIONS = ["light", "dark"]
AUTH_PROVIDER_OPTIONS = ["google", "facebook"]


class Settings(BaseSettings):
    PROJECT_NAME: str = "FastAPI Customer Care Server"
    API_V1_STR: str = "/api/v1"
    DATABASE_URL: str = "postgresql://postgres:postgres@localhost:5432/customer_care_db"
    ENVIRONMENT: str = "development"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )


settings = Settings()
