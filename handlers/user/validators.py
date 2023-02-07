import re


def validate_name(message):
    """Валидация введенных данных в поле Имя."""
    return (re.fullmatch(
        r"^[a-яА-ЯЁёa-zA-Z\s]{1,200}$",
        message
    ) and len(message) <= 200)


def validate_birthday(message):
    """Валидация введенных данных в поле даты рождения."""
    return re.fullmatch(
        r"^((0[1-9]|[12]\d)\.(0[1-9]|1[012])|"
        r"30\.(0[13-9]|1[012])|31\.(0[13578]|1[02]))$",
        message)


def validate_comment(message):
    """Валидация введенных данных в поле комментарий."""
    return (re.fullmatch(
        r"^[a-яА-ЯЁёa-zA-Z\s]{1,200}$",
        message
    ) and len(message) <= 200)
