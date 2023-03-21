from aiogram.types import (KeyboardButton, ReplyKeyboardMarkup,
                           ReplyKeyboardRemove)
from config import SUB_BUTTON_NAME

reg_button = "Регистрация"
add_new_note = "Добавить запись"
my_birthdays_button = "Мои записи"
cancel_button = "Отмена"
in_main_menu = "В главное меню"
today_birthday = "ДР сегодня"
delete_button = "Удалить"
time_setting = "Время рассылки"

time_1 = "07:00"
time_2 = "09:00"
time_3 = "11:00"
time_4 = "13:00"
time_5 = "15:00"
time_6 = "17:00"


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
        KeyboardButton(my_birthdays_button),
    )
    markup.row(
        KeyboardButton(today_birthday),
        KeyboardButton(time_setting),
    )
    return markup


def time_reply_keyboard():
    """Клавиатура выбора времени рассылки"""
    markup = ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
    markup.row(
        KeyboardButton(time_1),
        KeyboardButton(time_2),
        KeyboardButton(time_3),
    )
    markup.row(
        KeyboardButton(time_4),
        KeyboardButton(time_5),
        KeyboardButton(time_6),
    )
    markup.row(
        KeyboardButton(in_main_menu),
    )
    return markup


def canсel_keyboard():
    """Клавиатура отмены процесса."""
    markup = ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
    markup.add(KeyboardButton(cancel_button))
    return markup
