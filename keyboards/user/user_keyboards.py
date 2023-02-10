from aiogram.types import (KeyboardButton, ReplyKeyboardMarkup,
                           ReplyKeyboardRemove)
from data.services import is_admin

reg_button = "Регистрация"
add_new_note = "Добавить ДР"
my_birthdays_button = "Мои ДР"
cancel_button = "Отмена"
admin_menu_button = "Меню админа"


def remove_keyboard():
    """Удалить клавиатуру."""
    markup = ReplyKeyboardRemove()
    return markup


def reg_keyboard():
    """Клавиатура регистрации."""
    markup = ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
    markup.add(KeyboardButton(reg_button))
    return markup


def menu_reply_keyboard(telegram_id: int):
    """Клавиатура главного меню юзера."""
    markup = ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
    markup.row(KeyboardButton(add_new_note),
               KeyboardButton(my_birthdays_button))
    if is_admin(telegram_id):
        markup.row(KeyboardButton(admin_menu_button),)
    return markup


def canсel_keyboard():
    """Клавиатура отмены процесса."""
    markup = ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
    markup.add(KeyboardButton(cancel_button))
    return markup
