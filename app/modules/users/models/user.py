
from datetime import UTC, datetime

from beanie import Document
from pydantic import Field
from pymongo import ASCENDING, IndexModel


class UserDocument(Document):
    telegram_id: int

    timezone: str = "UTC"
    language: str = "en"

    created_at: datetime = Field(
        default_factory=lambda: datetime.now(UTC)
    )

    class Settings:
        name = "users"
        indexes = [
            IndexModel(
                [("telegram_id", ASCENDING)],
                unique=True,
            )
        ]
