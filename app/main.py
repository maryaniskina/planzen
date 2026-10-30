
from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.core.config import settings
from app.database.mongodb import mongodb
from app.health.api import router as health_router
from app.tasks.api import router as task_router


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    try:
        await mongodb.connect()
        yield
    finally:
        await mongodb.close()


app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    debug=settings.debug,
    lifespan=lifespan,
)

app.include_router(health_router)
app.include_router(task_router, prefix='/api')
