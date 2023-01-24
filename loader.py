import logging
import os

from aiogram import Bot
from aiogram.dispatcher import Dispatcher
from dotenv import load_dotenv

load_dotenv()

logging.basicConfig(level=logging.INFO)

TELEGRAM_TOKEN = os.getenv("T_TOKEN")

bot = Bot(token=TELEGRAM_TOKEN)
dp = Dispatcher(bot)
