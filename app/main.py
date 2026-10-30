
from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

from aiogram import Bot
from fastapi import FastAPI

from app.core.config import settings
from app.database.mongodb import mongodb
from app.health.api import router as health_router
from app.tasks.api import router as task_router
from app.telegram.dispatcher import dispatcher
from app.telegram.keyboards.main import get_main_menu_button
from app.telegram.webhook import router as telegram_router


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    bot = Bot(token=settings.telegram_bot_token.get_secret_value())
    app.state.telegram_bot = bot
    app.state.telegram_dispatcher = dispatcher

    webhook_url = (
        f'{settings.telegram_base_url.rstrip("/")}'
        f'{settings.telegram_webhook_path}'
    )
    try:
        await bot.set_chat_menu_button(
            menu_button=get_main_menu_button(),
        )
        await bot.set_webhook(
            url=webhook_url,
            secret_token=settings.telegram_webhook_secret.get_secret_value(),
            allowed_updates=dispatcher.resolve_used_update_types(),
        )
        await mongodb.connect()
        yield
    finally:
        await mongodb.close()


app = FastAPI(
    title=settings.app_name,
    debug=settings.debug,
    lifespan=lifespan,
)

app.include_router(health_router)
app.include_router(task_router, prefix='/api')
app.include_router(telegram_router)
