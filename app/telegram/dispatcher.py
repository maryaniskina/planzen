from aiogram import Dispatcher

from app.telegram.handlers.start import router as start_router

dispatcher = Dispatcher()
dispatcher.include_router(start_router)
