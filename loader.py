import logging
import os

import aiohttp
from aiogram import Bot
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import Dispatcher
from dotenv import load_dotenv

load_dotenv()

logging.basicConfig(level=logging.INFO)

TELEGRAM_TOKEN = os.getenv("T_TOKEN")
ADMIN = int(os.getenv("ADMIN_ID"))
CF_GROUP = list(map(int, os.getenv("CF_GROUP").split()))

storage = MemoryStorage()
# sock_connect ограничивает и TLS-рукопожатие: зависшее соединение
# обрывается за 10 секунд вместо 60, и отправку можно повторить.
bot = Bot(token=TELEGRAM_TOKEN,
          timeout=aiohttp.ClientTimeout(total=30, sock_connect=10))
dp = Dispatcher(bot, storage=storage)
