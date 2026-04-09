from typing import ClassVar
from pathlib import Path
from pydantic import Field
from pydantic_settings import BaseSettings
from infra.core.logs_backend import LoggerManager
# from azure.identity import DefaultAzureCredential, AzureAuthorityHosts
import logging

_ENV_FILE = Path(__file__).resolve().parents[4] / ".env"

class Settings(BaseSettings):
    # DATABASE_URL: str = "postgresql+asyncpg://postgres:postgres@localhost:5432/app"
    DB_URL: str = "sqlite+aiosqlite:///./app.db"
    AZURE_ENDPOINT : str | None = None
    OPENAI_API_VERSION : str | None = None
    OPENAI_DEPLOYMENT_NAME : str | None = None
    API_KEY : str | None = None
    logger: ClassVar[logging.Logger] = LoggerManager.get_logger()

    class Config:
        env_file = str(_ENV_FILE) if _ENV_FILE.exists() else None
        env_file_encoding = "utf-8"
        case_sensitive = True
        extra = "ignore"
        populate_by_name = True

settings = Settings()
# credential = DefaultAzureCredential(authority=AzureAuthorityHosts.AZURE_PUBLIC_CLOUD)
