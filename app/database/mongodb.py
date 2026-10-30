
from pymongo import AsyncMongoClient

from app.core.config import settings
from app.modules.users.models.models import UserDocument


class MongoDB:
    def __init__(self) -> None:
        self.client: AsyncMongoClient | None = None

    async def connect(self) -> None:
        self.client = AsyncMongoClient(
            settings.mongodb_uri,
            serverSelectionTimeoutMS=5000,
        )

        await self.client.admin.command("ping")

        from beanie import init_beanie

        await init_beanie(
            database=self.client[settings.mongodb_database],
            document_models=[UserDocument],
        )

    async def close(self) -> None:
        if self.client is not None:
            await self.client.close()
            self.client = None


mongodb = MongoDB()
