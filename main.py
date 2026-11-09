import asyncio
import logging

import aioschedule
from aiogram.utils import executor

from data.create_db import create_db
from data.db_loader import db_session
from data.sender import send_message_with_retry
from data.services import (future_birthdays_schedule_sendler,
                           today_birthdays_schedule_sendler)
from handlers.other import other_handlers
from handlers.user import user_handlers
from keyboards import time_1, time_2, time_3, time_4, time_5, time_6
from loader import ADMIN, dp

logger = logging.getLogger(__name__)


async def on_startup(_):
    """Выполняется при старте бота."""
    loop = asyncio.get_event_loop()
    loop.create_task(scheduler())
    try:
        await send_message_with_retry(ADMIN, 'Бот запущен')
    except Exception:
        pass  # причина уже в логе; без этого сообщения бот работает
    await create_db()


async def scheduler():
    """Расписание выполнения задач."""
    # время в UTC (часовой пояс контейнера), подписи time_N — московские
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
    scheduler.every().day.at("04:01").do(future_birthdays_schedule_sendler,
                                         time=time_1)
    scheduler.every().day.at("06:01").do(future_birthdays_schedule_sendler,
                                         time=time_2)
    scheduler.every().day.at("08:01").do(future_birthdays_schedule_sendler,
                                         time=time_3)
    scheduler.every().day.at("10:01").do(future_birthdays_schedule_sendler,
                                         time=time_4)
    scheduler.every().day.at("12:01").do(future_birthdays_schedule_sendler,
                                         time=time_5)
    scheduler.every().day.at("15:01").do(future_birthdays_schedule_sendler,
                                         time=time_6)
    while True:
        await scheduler.run_pending()
        await asyncio.sleep(1)


async def on_handler_error(update, exception):
    """Сбой в обработчике: в лог и откат сеанса базы, он один на весь бот."""
    logger.error(f'Сбой при обработке сообщения: {exception!r}',
                 exc_info=exception)
    db_session.rollback()
    return True


user_handlers.register_user_handlers(dp)
other_handlers.register_other_handlers(dp)
dp.register_errors_handler(on_handler_error)

executor.start_polling(dp, skip_updates=True, on_startup=on_startup)
