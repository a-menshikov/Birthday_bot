import csv
from .db_loader import db_session
from .models import User, Birthday, UserSubscribe, Birthday_CF, Subscribe
from sqlalchemy.sql import exists
from loader import ADMIN, bot
from config import private_sub, SUB_KIND


def is_user_exist_in_base(telegram_id: int) -> bool:
    """Проверка наличию пользователя в базе (таблица users)."""
    session = db_session()
    check = session.query(exists().where(
        User.telegram_id == telegram_id)).scalar()
    if check:
        return True
    return False


async def input_c_birthdays_in_base():
    """Загрузить в базу данные о ДР в Ц."""
    path = 'data/Ц.csv'

    with open(path, encoding='1251', mode='r') as file:
        csv_read = csv.DictReader(file, delimiter=';')
        counter = 0
        for i in csv_read:
            data = {}
            data['name'] = i['Сотрудник']
            data['row_birth_date'] = i['Дата рождения']
            data['division'] = i['Подразделение организации']
            data['position'] = i['Должность']
            b_date_tuple = tuple(map(int, i['Дата рождения'].split('.')))
            data['day_of_birth'] = b_date_tuple[0]
            data['month_of_birth'] = b_date_tuple[1]
            data['year_of_birth'] = b_date_tuple[2]
            try:
                create_new_birthday_note_cf(data)
                counter += 1
            except Exception as error:
                print(error)
                continue
        await bot.send_message(ADMIN, 'all ЦФ done')


def is_admin(telegram_id: int):
    """Проверка на админа."""
    return telegram_id == ADMIN


def all_sub_check(telegram_id: int) -> dict:
    """Проверка состояния подписок."""
    sub_status = {}

    for sub in SUB_KIND.keys():
        sub_status[sub] = False

    session = db_session()
    user_db_id = get_user_base_id(telegram_id)
    user_subs = session.query(UserSubscribe.subscribe,
                              Subscribe.name,
                              ).join(Subscribe).filter(
                                    UserSubscribe.user_id == user_db_id,
                                    UserSubscribe.status == 1
                                    ).all()

    for user_sub in user_subs:
        sub_status[user_sub[1]] = True

    return sub_status


def get_user_base_id(telegram_id: int) -> int:
    """Получить id пользователя в базе (таблица users)."""
    session = db_session()
    user_db_id = session.query(User.id).filter(
        User.telegram_id == telegram_id).one()[0]
    return user_db_id


def get_sub_base_id(sub_kind: str) -> int:
    """Получить id пользователя в базе (таблица users)."""
    session = db_session()
    sub_db_id = session.query(Subscribe.id).filter(
        Subscribe.name == sub_kind).one()[0]
    return sub_db_id


def create_new_user(telegram_id: int) -> None:
    """Создание нового пользователя"""
    session = db_session()
    new_user = User(telegram_id=telegram_id)
    session.add(new_user)
    session.commit()
    create_new_subscribe(telegram_id, private_sub)


def create_new_subscribe(telegram_id: int, sub_kind: str) -> None:
    """Создание подписки для пользователя"""
    session = db_session()
    user_id = get_user_base_id(telegram_id)
    sub_id = get_sub_base_id(sub_kind)
    new_subscribe = UserSubscribe(user_id=user_id, subscribe=sub_id, status=1)
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


def create_new_birthday_note_cf(data: dict) -> None:
    """Создание новой записи о дне рождения ЦФ."""
    session = db_session()
    check = session.query(Birthday_CF).filter(
        Birthday_CF.name == data['name'],
        Birthday_CF.row_birth_date == data['row_birth_date']).all()
    if not check:
        new_note = Birthday_CF(**data)
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
