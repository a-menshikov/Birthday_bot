from .db_loader import db_session
from .models import User, Birthday, UserSubscribe
from sqlalchemy.sql import exists


def is_user_exist_in_base(telegram_id: int) -> bool:
    """Проверка наличию пользователя в базе (таблица users)."""
    session = db_session()
    check = session.query(exists().where(
        User.telegram_id == telegram_id)).scalar()
    if check:
        return True
    return False


def get_user_base_id(telegram_id: int) -> bool:
    """Получить id пользователя в базе (таблица users)."""
    session = db_session()
    user_db_id = session.query(User.id).filter(
        User.telegram_id == telegram_id).one()[0]
    return user_db_id


def create_new_user(telegram_id: int) -> None:
    """Создание нового пользователя"""
    session = db_session()
    new_user = User(telegram_id=telegram_id)
    session.add(new_user)
    session.commit()
    create_new_private_subscribe(telegram_id)


def create_new_private_subscribe(telegram_id: int) -> None:
    """Создание приватной подписки для пользователя"""
    session = db_session()
    user_id = get_user_base_id(telegram_id)
    new_subscribe = UserSubscribe(user_id=user_id, subscribe=1, status=1)
    session.add(new_subscribe)
    session.commit()


def create_new_birthday_note(data: dict) -> None:
    """Создание новой записи о дне рождения."""
    session = db_session()
    new_note = Birthday(owner_id=data['owner_id'],
                        name=data['name'],
                        day_of_birth=data['day_of_birth'],
                        month_of_birth=data['month_of_birth'],
                        comment=data['comment'])
    session.add(new_note)
    session.commit()
