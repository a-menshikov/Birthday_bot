import csv
import datetime

from config import SUB_KIND, cf_sub, private_sub, timezone
from loader import ADMIN, CF_GROUP, bot
from sqlalchemy.sql import exists

from .db_loader import db_session
from .models import Birthday, BirthdayCF, Subscribe, User, UserSubscribe


def is_user_exist_in_base(telegram_id: int) -> bool:
    """Проверка наличию пользователя в базе (таблица users)."""
    check = db_session.query(exists().where(
        User.id == telegram_id)).scalar()
    if check:
        return True
    return False


async def input_c_birthdays_in_base():
    """Загрузить в базу данные о ДР в Ц."""
    path = 'db/Ц.csv'

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

    user_subs = db_session.query(UserSubscribe.subscribe,
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
    today_full_date = datetime.datetime.now(timezone).date()
    today_day = today_full_date.day
    today_month = today_full_date.month
    return db_session.query(
        BirthdayCF.division,
        BirthdayCF.position,
        BirthdayCF.name,
        BirthdayCF.row_birth_date,
        ).filter(BirthdayCF.day_of_birth == today_day,
                 BirthdayCF.month_of_birth == today_month,
                 ).all()


def get_today_birthdays_private(telegram_id: int):
    """Сегодняшние ДР в таблице приватных др."""
    today_full_date = datetime.datetime.now(timezone).date()
    today_day = today_full_date.day
    today_month = today_full_date.month
    return db_session.query(
        Birthday.name,
        Birthday.row_birth_date,
        ).filter(Birthday.day_of_birth == today_day,
                 Birthday.month_of_birth == today_month,
                 Birthday.owner_id == telegram_id,
                 ).all()


def make_today_bd_message(telegram_id: int):
    subscribe_status = all_sub_check(telegram_id)
    today_full_date = datetime.datetime.now(timezone).date()
    base_message = f'Дата: {today_full_date}\n\n'
    empty = True

    if subscribe_status[private_sub]:
        private = get_today_birthdays_private(telegram_id)
        base_message += 'ДНИ РОЖДЕНИЯ СЕГОДНЯ:\n\n'
        if private:
            for i in private:
                add_message = (f'{i[0]}\n'
                               f'{i[1]}\n\n'
                               )
                base_message += add_message
                if empty:
                    empty = False
        else:
            base_message += 'Сегодня нет дней рождения\n\n'

    if subscribe_status[cf_sub]:
        cf = get_today_birthdays_cf()
        base_message += 'В ЦЕНТРОФИНАНСЕ:\n\n'
        if cf:
            for i in cf:
                add_message = (f'{i[0]}\n'
                               f'{i[1]}\n'
                               f'{i[2]}\n'
                               f'{i[3]}\n\n'
                               )
                base_message += add_message
                if empty:
                    empty = False
        else:
            base_message += 'Сегодня нет дней рождения\n'

    return base_message, empty


async def today_birthdays_schedule_sendler():
    """Ежедневная рассылка."""
    users = get_all_users()
    if not users:
        return
    for i in users:
        user_id = i[0]
        base_message, empty = make_today_bd_message(user_id)
        if not empty:
            try:
                await bot.send_message(user_id, base_message)
            except Exception:
                continue


def get_sub_base_id(sub_kind: str) -> int:
    """Получить id подписки в базе"""
    return db_session.query(Subscribe.id).filter(
        Subscribe.name == sub_kind).one()[0]


def get_all_users():
    """Получить id подписки в базе"""
    return db_session.query(User.id).all()


def create_new_user(telegram_id: int) -> None:
    """Создание нового пользователя"""
    new_user = User(id=telegram_id)
    db_session.add(new_user)
    db_session.commit()
    create_new_subscribe(telegram_id, private_sub)
    if telegram_id in CF_GROUP:
        create_new_subscribe(telegram_id, cf_sub)


def create_new_subscribe(telegram_id: int, sub_kind: str) -> None:
    """Создание подписки для пользователя"""
    sub_id = get_sub_base_id(sub_kind)
    new_subscribe = UserSubscribe(user_id=telegram_id,
                                  subscribe=sub_id,
                                  status=1
                                  )
    db_session.add(new_subscribe)
    db_session.commit()


def create_new_birthday_note(data: dict) -> None:
    """Создание новой записи о дне рождения."""
    new_note = Birthday(owner_id=data['owner_id'],
                        name=data['name'],
                        row_birth_date=data['row_birth_date'],
                        day_of_birth=data['day_of_birth'],
                        month_of_birth=data['month_of_birth'],
                        )
    db_session.add(new_note)
    db_session.commit()


def create_new_birthday_note_cf(data: dict) -> None:
    """Создание новой записи о дне рождения ЦФ."""
    check = db_session.query(BirthdayCF).filter(
        BirthdayCF.name == data['name'],
        BirthdayCF.row_birth_date == data['row_birth_date']).all()
    if not check:
        new_note = BirthdayCF(**data)
        db_session.add(new_note)
        db_session.commit()


def delete_birthday_note(id: int) -> None:
    """Удаление записи о дне рождения."""
    check = db_session.query(Birthday).filter(
        Birthday.id == id).all()
    if not check:
        raise ValueError('Нет такой записи')
    db_session.delete(check[0])
    db_session.commit()


def view_users_birthday_notes(telegram_id: int) -> None:
    """Запрос из базы всех записей о ДР конкретного пользователя
    Возвращает список кортежей."""
    return db_session.query(
        Birthday.id,
        Birthday.name,
        Birthday.row_birth_date
        ).where(
        Birthday.owner_id == telegram_id).all()
