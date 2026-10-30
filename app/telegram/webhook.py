import secrets

from aiogram.types import Update
from fastapi import APIRouter, Header, HTTPException, Request, status
from fastapi.responses import Response

from app.core.config import settings


router = APIRouter()


@router.post(settings.telegram_webhook_path, include_in_schema=False)
async def telegram_webhook(
    request: Request,
    x_telegram_bot_api_secret_token: str | None = Header(default=None),
) -> Response:
    expected_secret = settings.telegram_webhook_secret.get_secret_value()

    if (
        x_telegram_bot_api_secret_token is None
        or not secrets.compare_digest(
            x_telegram_bot_api_secret_token,
            expected_secret,
        )
    ):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail='Invalid webhook secret',
        )

    bot = request.app.state.telegram_bot
    dispatcher = request.app.state.telegram_dispatcher

    payload = await request.json()

    update = Update.model_validate(
        payload,
        context={'bot': bot},
    )

    await dispatcher.feed_update(bot, update)

    return Response(status_code=status.HTTP_200_OK)
