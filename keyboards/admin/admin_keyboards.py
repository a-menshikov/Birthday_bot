from aiogram.types import KeyboardButton, ReplyKeyboardMarkup
from keyboards.user.user_keyboards import in_main_menu


def menu_admin_keyboard():
    """Клавиатура главного меню админа."""
    markup = ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
    markup.row(KeyboardButton(in_main_menu),)
    return markup
