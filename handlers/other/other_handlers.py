from aiogram import types
from aiogram.dispatcher import Dispatcher
from data.services import is_user_exist_in_base
from keyboards import menu_reply_keyboard, reg_keyboard


async def unknown_message(message: types.Message):
    """Любое неизвестное сообщение"""
    telegram_id = message.from_user.id
    checker = is_user_exist_in_base(telegram_id)
    if checker:
        await message.answer("Моя твоя не понимать",
                             reply_markup=menu_reply_keyboard())
    else:
        await message.answer("Моя твоя не понимать. "
                             "Давай-ка лучше зарегистрируемся?",
                             reply_markup=reg_keyboard())


def register_other_handlers(dp: Dispatcher):
    dp.register_message_handler(unknown_message)
