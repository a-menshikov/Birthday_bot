import asyncio

import aioschedule
from aiogram.utils import executor

from data.create_db import create_db
from data.services import (future_birthdays_schedule_sendler,
                           today_birthdays_schedule_sendler)
from handlers.other import other_handlers
from handlers.user import user_handlers
from keyboards import time_1, time_2, time_3, time_4, time_5, time_6
from loader import ADMIN, bot, dp


async def on_startup(_):
    """Выполняется при старте бота."""
    loop = asyncio.get_event_loop()
    loop.create_task(scheduler())
    await bot.send_message(ADMIN, 'Бот запущен')
    await create_db()


async def scheduler():
    """Расписание выполнения задач."""
    scheduler = aioschedule.Scheduler()
    scheduler.every().day.at("04:00").do(today_birthdays_schedule_sendler,
                                         time=time_1)
    scheduler.every().day.at("06:00").do(today_birthdays_schedule_sendler,
                                         time=time_2)
    scheduler.every().day.at("08:00").do(today_birthdays_schedule_sendler,
                                         time=time_3)
    scheduler.every().day.at("10:00").do(today_birthdays_schedule_sendler,
                                         time=time_4)
    scheduler.every().day.at("12:00").do(today_birthdays_schedule_sendler,
                                         time=time_5)
    scheduler.every().day.at("15:00").do(today_birthdays_schedule_sendler,
                                         time=time_6)
    scheduler.every().day.at("04:00").do(future_birthdays_schedule_sendler,
                                         time=time_1)
    scheduler.every().day.at("06:00").do(future_birthdays_schedule_sendler,
                                         time=time_2)
    scheduler.every().day.at("08:00").do(future_birthdays_schedule_sendler,
                                         time=time_3)
    scheduler.every().day.at("10:00").do(future_birthdays_schedule_sendler,
                                         time=time_4)
    scheduler.every().day.at("12:00").do(future_birthdays_schedule_sendler,
                                         time=time_5)
    scheduler.every().day.at("15:00").do(future_birthdays_schedule_sendler,
                                         time=time_6)
    while True:
        await scheduler.run_pending()
        await asyncio.sleep(1)

user_handlers.register_user_handlers(dp)
other_handlers.register_other_handlers(dp)

executor.start_polling(dp, skip_updates=True, on_startup=on_startup)
