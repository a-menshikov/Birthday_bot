from aiogram.types import (KeyboardButton, ReplyKeyboardMarkup,
                           ReplyKeyboardRemove)

reg_button = "Регистрация"
add_new_note = "Добавить запись ДР"
my_birthdays_button = "Мои записи о ДР"
cancel_button = "Отмена"


def remove_keyboard():
    markup = ReplyKeyboardRemove()
    return markup


def reg_keyboard():
    markup = ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
    markup.add(KeyboardButton(reg_button))
    return markup


def menu_reply_keyboard():
    markup = ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
    markup.add(KeyboardButton(add_new_note))
    markup.add(KeyboardButton(my_birthdays_button))
    return markup


def canсel_keyboard():
    markup = ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
    markup.add(KeyboardButton(cancel_button))
    return markup
