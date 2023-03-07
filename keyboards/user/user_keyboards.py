from aiogram.types import (KeyboardButton, ReplyKeyboardMarkup,
                           ReplyKeyboardRemove)
from data.services import is_admin
from config import SUB_BUTTON_NAME

reg_button = "Регистрация"
add_new_note = "Добавить ДР"
my_birthdays_button = "Мои ДР"
cancel_button = "Отмена"
in_main_menu = "В главное меню"
admin_menu_button = "Меню админа"
subscribes = "Подписки"
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
        button = f'{SUB_BUTTON_NAME[i[0]]} - подписка'
        if i[1]:
            button = f'{SUB_BUTTON_NAME[i[0]]} - отписка'
        markup.add(KeyboardButton(button))
    markup.add(KeyboardButton(in_main_menu))
    return markup


def menu_reply_keyboard(telegram_id: int):
    """Клавиатура главного меню юзера."""
    markup = ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
    markup.row(
        KeyboardButton(add_new_note),
        KeyboardButton(my_birthdays_button),
    )
    markup.row(
        KeyboardButton(subscribes),
        KeyboardButton(today_birthday),
    )
    if is_admin(telegram_id):
        markup.row(KeyboardButton(admin_menu_button),)
    return markup


def canсel_keyboard():
    """Клавиатура отмены процесса."""
    markup = ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
    markup.add(KeyboardButton(cancel_button))
    return markup
