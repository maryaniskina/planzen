
from functools import lru_cache

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        case_sensitive=False,
        extra="ignore",
    )

    app_name: str = "Planzen"
    app_version: str = "0.1.0"
    debug: bool = False

    mongodb_uri: str = Field(...)
    mongodb_database: str = "planzen"


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
