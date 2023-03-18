import asyncio

import aioschedule
from aiogram.utils import executor

from data.create_db import create_db
from data.services import today_birthdays_schedule_sendler
from handlers.other import other_handlers
from handlers.user import user_handlers
from loader import ADMIN, bot, dp


async def on_startup(_):
    """Выполняется при старте бота."""
    loop = asyncio.get_event_loop()
    loop.create_task(scheduler())
    await bot.send_message(ADMIN, 'Бот запущен')
    await create_db()


async def scheduler():
    """Расписание выполнения задач."""
    aioschedule.every().day.at("06:00").do(today_birthdays_schedule_sendler)
    while True:
        await aioschedule.run_pending()
        await asyncio.sleep(1)

user_handlers.register_user_handlers(dp)
other_handlers.register_other_handlers(dp)

executor.start_polling(dp, skip_updates=True, on_startup=on_startup)
