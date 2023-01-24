from .db_loader import db_session
from .models import User


def is_user_exist_in_base(telegram_id: int) -> bool:
    """Проверка наличию пользователя в базе (таблица users)."""
    session = db_session()
    check = session.query(User).filter(
        User.telegram_id == telegram_id).all()
    if check:
        return True
    return False


def create_new_user(telegram_id: int) -> None:
    """Создание нового пользователя"""
    session = db_session()
    new_user = User(telegram_id=telegram_id)
    session.add(new_user)
    session.commit()
