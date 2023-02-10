from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

input_base = "Залить ДР Ц"
user_menu = "/start"


def menu_admin_keyboard():
    """Клавиатура главного меню админа."""
    markup = ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
    markup.row(KeyboardButton(input_base),)
    markup.row(KeyboardButton(user_menu),)
    return markup
