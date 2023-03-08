from aiogram.types import (KeyboardButton, ReplyKeyboardMarkup,
                           ReplyKeyboardRemove)
from config import SUB_BUTTON_NAME

reg_button = "Регистрация"
add_new_note = "Добавить ДР"
my_birthdays_button = "Мои ДР"
cancel_button = "Отмена"
in_main_menu = "В главное меню"
today_birthday = "ДР сегодня"


def remove_keyboard():
    """Удалить клавиатуру."""
    markup = ReplyKeyboardRemove()
    return markup


def reg_keyboard():
    """Клавиатура регистрации."""
    markup = ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
    markup.add(KeyboardButton(reg_button))
    return markup


def sub_keyboard(data: dict):
    """Клавиатура подписок."""
    markup = ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
    for i in data.items():
        button = f'{SUB_BUTTON_NAME[i[0]]} - подписаться'
        if i[1]:
            button = f'{SUB_BUTTON_NAME[i[0]]} - отписаться'
        markup.add(KeyboardButton(button))
    markup.add(KeyboardButton(in_main_menu))
    return markup


def menu_reply_keyboard():
    """Клавиатура главного меню юзера."""
    markup = ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
    markup.row(
        KeyboardButton(add_new_note),
    )
    markup.row(
        KeyboardButton(my_birthdays_button),
        KeyboardButton(today_birthday),
    )
    return markup


def canсel_keyboard():
    """Клавиатура отмены процесса."""
    markup = ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
    markup.add(KeyboardButton(cancel_button))
    return markup
