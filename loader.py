import logging
import os
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram import Bot
from aiogram.dispatcher import Dispatcher
from dotenv import load_dotenv

load_dotenv()

logging.basicConfig(level=logging.INFO)

TELEGRAM_TOKEN = os.getenv("T_TOKEN")
ADMIN = os.getenv("ADMIN_ID")

storage = MemoryStorage()
bot = Bot(token=TELEGRAM_TOKEN)
dp = Dispatcher(bot, storage=storage)
