from aiogram import types
from aiogram.dispatcher import Dispatcher
from data.services import create_new_user, is_user_exist_in_base
from keyboards import (menu_button, menu_inline_keyboard, menu_keyboard,
                       reg_button, reg_keyboard)


async def starter(message: types.Message):
    """Ответы на команды start и help"""
    telegram_id = message.from_user.id
    checker = is_user_exist_in_base(telegram_id)
    if checker:
        await message.answer("Привет. Этот бот умеет напоминать о ДР",
                             reply_markup=menu_keyboard())
    else:
        await message.answer("Привет. Этот бот умеет напоминать о ДР."
                             "Жми кнопку и начнём!",
                             reply_markup=reg_keyboard())


async def registration(message: types.Message):
    """Регистрация нового пользователя."""
    telegram_id = message.from_user.id
    checker = is_user_exist_in_base(telegram_id)
    if checker:
        await message.answer("Вы уже зарегистрированы. Воспользуйтесь меню",
                             reply_markup=menu_keyboard())
    else:
        create_new_user(telegram_id)
        await message.answer("Welcome. Полный функционал доступен."
                             " Воспользуйтесь меню",
                             reply_markup=menu_keyboard())


async def menu_sendler(message: types.Message):
    await message.answer("Вот такое щаз меню",
                         reply_markup=menu_inline_keyboard())


def register_user_handlers(dp: Dispatcher):
    dp.register_message_handler(starter, commands=["start", "help"])
    dp.register_message_handler(registration, text=reg_button)
    dp.register_message_handler(menu_sendler, text=menu_button)
