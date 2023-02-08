from aiogram.types import (KeyboardButton, ReplyKeyboardMarkup,
                           ReplyKeyboardRemove)

reg_button = "Регистрация"
add_new_note = "Добавить ДР"
my_birthdays_button = "Мои ДР"
cancel_button = "Отмена"


def remove_keyboard():
    """Удалить клавиатуру."""
    markup = ReplyKeyboardRemove()
    return markup


def reg_keyboard():
    """Клавиатура регистрации."""
    markup = ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
    markup.add(KeyboardButton(reg_button))
    return markup


def menu_reply_keyboard():
    """Клавиатура главного меню."""
    markup = ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
    markup.row(KeyboardButton(add_new_note),
               KeyboardButton(my_birthdays_button))
    return markup


def canсel_keyboard():
    """Клавиатура отмены процесса."""
    markup = ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
    markup.add(KeyboardButton(cancel_button))
    return markup
