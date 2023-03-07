import datetime
import logging
import os

import pytz
from aiogram import Bot
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import Dispatcher
from dotenv import load_dotenv

load_dotenv()

logging.basicConfig(level=logging.INFO)

TELEGRAM_TOKEN = os.getenv("T_TOKEN")
ADMIN = int(os.getenv("ADMIN_ID"))

storage = MemoryStorage()
bot = Bot(token=TELEGRAM_TOKEN)
dp = Dispatcher(bot, storage=storage)

timezone_moscow = pytz.timezone("Etc/GMT-3")
today_full_date = datetime.datetime.now(timezone_moscow).date()
today_day = today_full_date.day
today_month = today_full_date.month
