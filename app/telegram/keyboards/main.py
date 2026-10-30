from aiogram.types import MenuButtonWebApp, WebAppInfo

from app.core.config import settings


def get_main_menu_button() -> MenuButtonWebApp:
    return MenuButtonWebApp(
        text='Открыть приложение',
        web_app=WebAppInfo(
            url=settings.telegram_base_url,
        ),
    )
