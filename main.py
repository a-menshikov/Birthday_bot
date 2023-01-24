from aiogram.utils import executor
from data.create_db import create_db
from loader import dp
from handlers.user import handlers


async def on_startup(_):
    """Выполняется при старте бота."""
    create_db()

handlers.register_user_handlers(dp)

executor.start_polling(dp, skip_updates=True, on_startup=on_startup)
