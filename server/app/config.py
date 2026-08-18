import os
import enum
from pydantic_settings import BaseSettings, SettingsConfigDict

class THEME_OPTIONS(str, enum.Enum):
    dark = "dark"
    lite = "lite"

class AUTH_PROVIDER_OPTIONS(str, enum.Enum):
    google = "google",
    facebook = "facebook"
    credentials_provider = "cradentaials-provider"


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
