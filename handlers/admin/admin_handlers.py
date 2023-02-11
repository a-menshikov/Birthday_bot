from aiogram import types
from aiogram.dispatcher import Dispatcher
from data.services import is_admin
from keyboards.user.user_keyboards import admin_menu_button
from keyboards.admin.admin_keyboards import menu_admin_keyboard


async def admin_begin(message: types.Message):
    """Вывод меню админа."""
    telegram_id = message.from_user.id
    checker = is_admin(telegram_id)
    if checker:
        await message.answer("Привет, Админ!",
                             reply_markup=menu_admin_keyboard())
    else:
        await message.answer("Чужак!!!")


def register_admin_handlers(dp: Dispatcher):
    dp.register_message_handler(admin_begin, text=admin_menu_button)
