from aiogram.types import (KeyboardButton, ReplyKeyboardMarkup,
                           ReplyKeyboardRemove)

reg_button = "Регистрация"
menu_button = "Меню"
add_new_note = "Добавить запись ДР"
cancel_button = "Отмена"


def remove_keyboard():
    markup = ReplyKeyboardRemove()
    return markup


def reg_keyboard():
    markup = ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
    markup.add(KeyboardButton(reg_button))
    return markup


def main_menu_keyboard():
    markup = ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
    markup.add(KeyboardButton(menu_button))
    return markup


def menu_reply_keyboard():
    markup = ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
    markup.add(KeyboardButton(add_new_note))
    return markup


def canсel_keyboard():
    markup = ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
    markup.add(KeyboardButton(cancel_button))
    return markup
