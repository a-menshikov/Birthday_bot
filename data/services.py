import csv

from config import SUB_KIND, private_sub, timezone, cf_sub
from loader import ADMIN, bot
from sqlalchemy.sql import exists
import datetime

from .db_loader import db_session
from .models import Birthday, Birthday_CF, Subscribe, User, UserSubscribe


def is_user_exist_in_base(telegram_id: int) -> bool:
    """Проверка наличию пользователя в базе (таблица users)."""
    session = db_session()
    check = session.query(exists().where(
        User.id == telegram_id)).scalar()
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
    user_subs = session.query(UserSubscribe.subscribe,
                              Subscribe.name,
                              ).join(Subscribe).filter(
                                    UserSubscribe.user_id == telegram_id,
                                    UserSubscribe.status == 1
                                    ).all()

    for user_sub in user_subs:
        sub_status[user_sub[1]] = True

    return sub_status


def get_today_birthdays_cf():
    """Сегодняшние ДР в таблице ЦФ"""
    session = db_session()
    today_full_date = datetime.datetime.now(timezone).date()
    today_day = today_full_date.day
    today_month = today_full_date.month
    result = session.query(
        Birthday_CF.division,
        Birthday_CF.position,
        Birthday_CF.name,
        Birthday_CF.row_birth_date,
        ).filter(Birthday_CF.day_of_birth == today_day,
                 Birthday_CF.month_of_birth == today_month,
                 ).all()
    return result


def get_today_birthdays_private(telegram_id: int):
    """Сегодняшние ДР в таблице приватных др."""
    session = db_session()
    today_full_date = datetime.datetime.now(timezone).date()
    today_day = today_full_date.day
    today_month = today_full_date.month
    result = session.query(
        Birthday.name,
        Birthday.row_birth_date,
        ).filter(Birthday.day_of_birth == today_day,
                 Birthday.month_of_birth == today_month,
                 Birthday.owner_id == telegram_id,
                 ).all()
    return result


def get_sub_base_id(sub_kind: str) -> int:
    """Получить id подписки в базе"""
    session = db_session()
    sub_db_id = session.query(Subscribe.id).filter(
        Subscribe.name == sub_kind).one()[0]
    return sub_db_id


def create_new_user(telegram_id: int) -> None:
    """Создание нового пользователя"""
    session = db_session()
    new_user = User(id=telegram_id)
    session.add(new_user)
    session.commit()
    create_new_subscribe(telegram_id, private_sub)
    create_new_subscribe(telegram_id, cf_sub)


def create_new_subscribe(telegram_id: int, sub_kind: str) -> None:
    """Создание подписки для пользователя"""
    session = db_session()
    sub_id = get_sub_base_id(sub_kind)
    new_subscribe = UserSubscribe(user_id=telegram_id,
                                  subscribe=sub_id,
                                  status=1
                                  )
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
                        )
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


def delete_birthday_note(id: int) -> None:
    """Удаление записи о дне рождения."""
    session = db_session()
    check = session.query(Birthday).filter(
        Birthday.id == id).all()
    if not check:
        raise ValueError('Нет такой записи')
    session.delete(check[0])
    session.commit()


def view_users_birthday_notes(telegram_id: int) -> None:
    """Запрос из базы всех записей о ДР конкретного пользователя
    Возвращает список кортежей."""
    session = db_session()
    notes = session.query(
        Birthday.id,
        Birthday.name,
        Birthday.row_birth_date
        ).where(
        Birthday.owner_id == telegram_id).all()
    session.commit()
    return notes
