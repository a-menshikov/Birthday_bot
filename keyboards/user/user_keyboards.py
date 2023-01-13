from aiogram.types import (InlineKeyboardButton, InlineKeyboardMarkup,
                           KeyboardButton, ReplyKeyboardMarkup)

reg_button = "Регистрация"
menu_button = "Меню"
button = "Какая-то кнопка"


def reg_keyboard():
    markup = ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
    markup.add(KeyboardButton(reg_button))
    return markup


def menu_keyboard():
    markup = ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
    markup.add(KeyboardButton(menu_button))
    return markup


def menu_inline_keyboard():
    markup = InlineKeyboardMarkup(resize_keyboard=True, selective=True)
    markup.add(InlineKeyboardButton(button, callback_data=button))
    return markup
