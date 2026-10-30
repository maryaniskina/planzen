from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message

router = Router()


@router.message(CommandStart())
async def start_handler(message: Message) -> None:
    await message.answer(
        'Привет! Это Planzen — твой персональный планировщик задач.\n\n'
        'Нажми кнопку ниже, чтобы открыть приложение.',
    )
