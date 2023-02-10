import csv
from .db_loader import db_session
from .models import User, Birthday, UserSubscribe
from sqlalchemy.sql import exists
from loader import ADMIN


def is_user_exist_in_base(telegram_id: int) -> bool:
    """Проверка наличию пользователя в базе (таблица users)."""
    session = db_session()
    check = session.query(exists().where(
        User.telegram_id == telegram_id)).scalar()
    if check:
        return True
    return False


def input_c_birthdays_in_base():
    """Загрузить в базу данные о ДР в Ц."""
    path = 'data/Ц.csv'
    session = db_session()

    with open(path, encoding='1251', mode='r') as file:
        csv_read = csv.DictReader(file, delimiter=';')
        for i in csv_read:
            pass


def is_admin(telegram_id: int):
    """Проверка на админа."""
    return telegram_id == ADMIN


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
                        row_birth_date=data['row_birth_date'],
                        day_of_birth=data['day_of_birth'],
                        month_of_birth=data['month_of_birth'],
                        comment=data['comment'])
    session.add(new_note)
    session.commit()


def view_users_birthday_notes(telegram_id: int) -> None:
    """Запрос из базы всех записей о ДР конкретного пользователя
    Возвращает список кортежей."""
    session = db_session()
    user_id = get_user_base_id(telegram_id)
    notes = session.query(
        Birthday.id,
        Birthday.name,
        Birthday.row_birth_date,
        Birthday.comment).where(
        Birthday.owner_id == user_id).all()
    session.commit()
    return notes
