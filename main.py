from aiogram.utils import executor
from data.create_db import create_db
from loader import dp, bot, ADMIN
from handlers.user import user_handlers
from handlers.other import other_handlers


async def on_startup(_):
    """Выполняется при старте бота."""
    await bot.send_message(ADMIN, 'Бот запущен')
    await create_db()

user_handlers.register_user_handlers(dp)
other_handlers.register_other_handlers(dp)

executor.start_polling(dp, skip_updates=True, on_startup=on_startup)
