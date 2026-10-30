
from functools import lru_cache

from pydantic import SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file='.env',
        env_file_encoding='utf-8',
        extra='ignore',
    )

    # Application
    app_name: str = 'Planzen'
    debug: bool = False

    # MongoDB
    mongodb_url: str
    mongodb_database: str = 'planzen'

    # Telegram
    telegram_bot_token: SecretStr
    telegram_webhook_secret: SecretStr
    telegram_base_url: str
    telegram_webhook_path: str = '/telegram/webhook'


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
