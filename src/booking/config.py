"""Application settings loaded from the environment."""

from functools import lru_cache
from typing import Literal

from pydantic import Field, PostgresDsn
from pydantic_settings import BaseSettings, SettingsConfigDict

LogLevel = Literal["debug", "info", "warning", "error"]
Environment = Literal["development", "test", "production"]


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="forbid",
        case_sensitive=False,
    )

    port: int = Field(default=8080, ge=1, le=65535)
    log_level: LogLevel = "info"
    environment: Environment = "development"
    app_version: str = "0.0.0-dev"

    database_url: PostgresDsn


@lru_cache
def get_settings() -> Settings:
    return Settings()  # type: ignore[call-arg]
