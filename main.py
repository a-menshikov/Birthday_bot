import logging
import os

from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from database import is_user_exist_in_base, new_user
from dotenv import load_dotenv
from keyboards import (menu_button, menu_inline_keyboard, menu_keyboard,
                       reg_button, reg_keyboard)

load_dotenv()

logging.basicConfig(level=logging.INFO)

TELEGRAM_TOKEN = os.getenv("T_TOKEN")

bot = Bot(token=TELEGRAM_TOKEN)
dp = Dispatcher(bot)


async def on_startup(_):
    """Выполняется при старте бота."""
    pass


@dp.message_handler(commands=["start", "help"])
async def starter(message: types.Message):
    """Ответы на команды start и help"""
    user_id = message.from_user.id
    checker = is_user_exist_in_base(user_id)
    if checker:
        await message.answer("Привет. Этот бот умеет напоминать о ДР",
                             reply_markup=menu_keyboard())
    else:
        await message.answer("Привет. Этот бот умеет напоминать о ДР."
                             "Жми кнопку и начнём!",
                             reply_markup=reg_keyboard())


@dp.message_handler(text=reg_button)
async def registration(message: types.Message):
    user_id = message.from_user.id
    checker = is_user_exist_in_base(user_id)
    if checker:
        await message.answer("Вы уже зарегистрированы. Воспользуйтесь меню",
                             reply_markup=menu_keyboard())
    else:
        new_user(user_id)
        await message.answer("Welcome. Полный функционал доступен."
                             " Воспользуйтесь меню",
                             reply_markup=menu_keyboard())


@dp.message_handler(text=menu_button)
async def menu_sendler(message: types.Message):
    await message.answer("Вот такое щаз меню",
                         reply_markup=menu_inline_keyboard())


executor.start_polling(dp, skip_updates=True, on_startup=on_startup)
