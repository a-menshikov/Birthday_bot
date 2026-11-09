import re

from aiogram.types import (KeyboardButton, ReplyKeyboardMarkup,
                           ReplyKeyboardRemove)
from config import future_days, SUB_BUTTON_NAME

reg_button = "Регистрация"
add_new_note = "Добавить запись"
my_birthdays_button = "Мои записи"
cancel_button = "Отмена"
in_main_menu = "В главное меню"
today_birthday = "ДР сегодня"
delete_button = "Удалить"
time_setting = "Время рассылки"
subscribes_button = "Подписки"
future_birthday = f"Ближайшие {future_days} дня"
subscribe_action = "подписаться"
unsubscribe_action = "отписаться"
# кнопки подписок вида «Персональная - отписаться»
sub_button_regexp = (
    f"^({'|'.join(re.escape(name) for name in SUB_BUTTON_NAME.values())})"
    f" - ({subscribe_action}|{unsubscribe_action})$"
)

time_1 = "07:00"
time_2 = "09:00"
time_3 = "11:00"
time_4 = "13:00"
time_5 = "15:00"
time_6 = "18:00"


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
    for sub_kind, subscribed in data.items():
        action = unsubscribe_action if subscribed else subscribe_action
        markup.add(KeyboardButton(f'{SUB_BUTTON_NAME[sub_kind]} - {action}'))
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
        KeyboardButton(future_birthday),
    )
    markup.row(
        KeyboardButton(time_setting),
        KeyboardButton(subscribes_button),
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
