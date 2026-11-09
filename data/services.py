import calendar
import csv
import datetime
import logging

from aiogram.utils.exceptions import BotBlocked, UserDeactivated
from config import (SUB_KIND, cf_sub, default_send_time, future_days,
                    private_sub, timezone)
from keyboards import menu_reply_keyboard
from loader import ADMIN, CF_GROUP
from sqlalchemy import and_, or_
from sqlalchemy.sql import exists

from .db_loader import db_session
from .models import (Birthday, BirthdayCF, Subscribe, User, UserSendTime,
                     UserSubscribe)
from .sender import send_message_with_retry

logger = logging.getLogger(__name__)


def is_user_exist_in_base(telegram_id: int) -> bool:
    """Проверка наличия пользователя в базе (таблица users)."""
    check = db_session.query(exists().where(
        User.id == telegram_id)).scalar()
    if check:
        return True
    return False


CF_FILE_COLUMNS = ('Подразделение организации', 'Должность', 'Сотрудник',
                   'Дата рождения')


async def check_c_birthdays_in_base():
    """Привести базу данных о ДР в Ц в соотвествие с файлом."""
    path = 'db/Ц.csv'

    # без файла или с чужими столбцами список не трогаем: сверка ниже удалила
    # бы из базы всех, кого нет в файле
    try:
        with open(path, encoding='1251', mode='r') as file:
            csv_read = csv.DictReader(file, delimiter=';')
            columns = csv_read.fieldnames or []
            rows = list(csv_read)
    except (OSError, UnicodeDecodeError, csv.Error) as error:
        await notify_admin(f'Файл ЦФ не прочитался, список ЦФ не обновлён: '
                           f'{error!r}')
        return
    missing = [column for column in CF_FILE_COLUMNS if column not in columns]
    if missing or not rows:
        await notify_admin(f'Файл ЦФ пустой или без столбцов {missing}, '
                           f'список ЦФ не обновлён')
        return

    # выбираем всех кто уже есть в базе из Ц
    all_cf_now = db_session.query(
        BirthdayCF.division,
        BirthdayCF.position,
        BirthdayCF.name,
        ).all()

    post_counter = 0
    bad_rows = 0
    for i in rows:
        checker = (
            i['Подразделение организации'],
            i['Должность'],
            i['Сотрудник'],
        )
        if checker in all_cf_now:
            # если уже есть в базе удаляем из чекера и пропускаем
            all_cf_now.remove(checker)
            continue
        try:
            day, month, year = map(int, i['Дата рождения'].split('.'))
            datetime.date(year, month, day)  # такая дата существует
            create_new_birthday_note_cf({
                'name': i['Сотрудник'],
                'row_birth_date': i['Дата рождения'],
                'division': i['Подразделение организации'],
                'position': i['Должность'],
                'day_of_birth': day,
                'month_of_birth': month,
                'year_of_birth': year,
            })
            post_counter += 1
        except Exception as error:
            db_session.rollback()
            bad_rows += 1
            logger.warning(f'Строка файла ЦФ пропущена: {error!r}')

    del_count = 0
    # всех кого не нашли в файле из базы удаляем
    for i in all_cf_now:
        check = db_session.query(BirthdayCF).filter(
            BirthdayCF.division == i[0],
            BirthdayCF.position == i[1],
            BirthdayCF.name == i[2],
        ).all()
        db_session.delete(check[0])
        db_session.commit()
        del_count += 1

    await notify_admin(f'all ЦФ done, создано {post_counter}, '
                       f'удалено {del_count}, пропущено строк {bad_rows}')


async def notify_admin(text: str) -> None:
    """Служебное сообщение админу; без него бот работает."""
    logger.info(text)
    try:
        await send_message_with_retry(ADMIN, text)
    except Exception:
        pass  # причина уже в логе


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


def birthday_on(model, date: datetime.date):
    """Условие «ДР в этот день»; 29.02 в невисокосный год — 28.02."""
    condition = and_(model.day_of_birth == date.day,
                     model.month_of_birth == date.month)
    if (date.month, date.day) == (2, 28) and not calendar.isleap(date.year):
        condition = or_(condition, and_(model.day_of_birth == 29,
                                        model.month_of_birth == 2))
    return condition


def get_today_birthdays_cf():
    """Сегодняшние ДР в таблице ЦФ"""
    today_full_date = datetime.datetime.now(timezone).date()
    return db_session.query(
        BirthdayCF.division,
        BirthdayCF.position,
        BirthdayCF.name,
        BirthdayCF.row_birth_date,
        ).filter(birthday_on(BirthdayCF, today_full_date)).all()


def get_today_birthdays_private(telegram_id: int):
    """Сегодняшние ДР в таблице приватных др."""
    today_full_date = datetime.datetime.now(timezone).date()
    return db_session.query(
        Birthday.name,
        Birthday.row_birth_date,
        ).filter(birthday_on(Birthday, today_full_date),
                 Birthday.owner_id == telegram_id,
                 ).all()


def get_future_birthdays_private(telegram_id: int):
    """Будущие ДР в таблице приватных др."""
    today_full_date = datetime.datetime.now(timezone).date()
    results = []
    for i in range(1, future_days + 1):
        current_date = today_full_date + datetime.timedelta(days=i)
        results.extend(db_session.query(
            Birthday.name,
            Birthday.row_birth_date,
        ).filter(birthday_on(Birthday, current_date),
                 Birthday.owner_id == telegram_id,
                 ).all())
    return results


def get_future_birthdays_cf():
    """Будущие ДР в таблице ЦФ."""
    today_full_date = datetime.datetime.now(timezone).date()
    results = []
    for i in range(1, future_days + 1):
        current_date = today_full_date + datetime.timedelta(days=i)
        results.extend(db_session.query(
            BirthdayCF.division,
            BirthdayCF.position,
            BirthdayCF.name,
            BirthdayCF.row_birth_date,
        ).filter(birthday_on(BirthdayCF, current_date)).all())
    return results


def make_today_bd_message(telegram_id: int):
    """Сформировать сообщение о сегодняшних ДР пользователя
    Возвращает кортеж - первый элемент: само сообщение,
    второй элемент: флаг пустого сообщения - если True, то
    ни одного ДР в сообщении нет."""
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
        base_message += 'В ЦФ:\n\n'
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


def make_future_bd_message(telegram_id: int):
    """Сформировать сообщение о будущих ДР пользователя
    Возвращает кортеж - первый элемент: само сообщение,
    второй элемент: флаг пустого сообщения - если True, то
    ни одного ДР в сообщении нет."""
    subscribe_status = all_sub_check(telegram_id)
    base_message = ''
    empty = True

    if subscribe_status[private_sub]:
        private = get_future_birthdays_private(telegram_id)
        base_message += f'ДНИ РОЖДЕНИЯ В БЛИЖАЙШИЕ {future_days} ДНЯ:\n\n'
        if private:
            for i in private:
                add_message = (f'{i[0]}\n'
                               f'{i[1]}\n\n'
                               )
                base_message += add_message
                if empty:
                    empty = False
        else:
            base_message += (f'В ближайшие {future_days} дня '
                             f'нет дней рождения\n\n')

    if subscribe_status[cf_sub]:
        cf = get_future_birthdays_cf()
        base_message += 'В ЦФ:\n\n'
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
            base_message += (f'В ближайшие {future_days} дня в ЦФ '
                             f'нет дней рождения\n\n')

    return base_message, empty


async def today_birthdays_schedule_sendler(time: str):
    """Ежедневная рассылка о сегодняшних ДР."""
    await send_birthdays(time, make_today_bd_message)


async def future_birthdays_schedule_sendler(time: str):
    """Ежедневная рассылка о ДР в ближайшие дни."""
    await send_birthdays(time, make_future_bd_message)


async def send_birthdays(time: str, make_message) -> None:
    """Разослать сообщение make_message пользователям с временем time."""
    # упавшую задачу aioschedule перезапускает каждую секунду, поэтому ловим всё
    try:
        for (user_id,) in get_all_users_with_fix_time(time):
            base_message, empty = make_message(user_id)
            if empty:
                continue
            try:
                await send_message_with_retry(
                    user_id, base_message, reply_markup=menu_reply_keyboard())
            except (BotBlocked, UserDeactivated):
                disable_subscriptions(user_id)
            except Exception:
                continue
    except Exception:
        logger.exception('Рассылка ДР прервалась')
        db_session.rollback()


def disable_subscriptions(telegram_id: int) -> None:
    """Снять все подписки пользователю, до которого бот не достучится."""
    db_session.query(UserSubscribe).filter(
        UserSubscribe.user_id == telegram_id).update(
            {'status': False}, synchronize_session='fetch')
    db_session.commit()
    logger.info(f'Пользователь {telegram_id} заблокировал бота или удалён, '
                f'подписки сняты')


def get_sub_base_id(sub_kind: str) -> int:
    """Получить id подписки в базе"""
    return db_session.query(Subscribe.id).filter(
        Subscribe.name == sub_kind).one()[0]


def get_all_users():
    """Получить id всех юзеров."""
    return db_session.query(User.id).all()


def get_all_users_with_fix_time(time: str):
    """Получить id всех юзеров с рассылкой на конкретное время."""
    return db_session.query(
        UserSendTime.user_id).filter(
            UserSendTime.time == time).all()


def create_new_user(telegram_id: int) -> None:
    """Создание нового пользователя"""
    new_user = User(id=telegram_id)
    db_session.add(new_user)
    db_session.commit()
    create_new_subscribe(telegram_id, private_sub)
    if telegram_id in CF_GROUP:
        create_new_subscribe(telegram_id, cf_sub)
    create_update_send_time(telegram_id, default_send_time)


def create_new_subscribe(telegram_id: int, sub_kind: str) -> None:
    """Создание подписки для пользователя"""
    sub_id = get_sub_base_id(sub_kind)
    new_subscribe = UserSubscribe(user_id=telegram_id,
                                  subscribe=sub_id,
                                  status=1
                                  )
    db_session.add(new_subscribe)
    db_session.commit()


def available_subscribes(telegram_id: int) -> dict:
    """Подписки для меню со статусом; ЦФ — только CF_GROUP и уже подписанным."""
    status = all_sub_check(telegram_id)
    if telegram_id not in CF_GROUP and not status[cf_sub]:
        del status[cf_sub]
    return status


def set_subscribe_status(telegram_id: int, sub_kind: str,
                         subscribed: bool) -> None:
    """Включить или отключить подписку; если её не было — создать."""
    sub_id = get_sub_base_id(sub_kind)
    updated = db_session.query(UserSubscribe).filter(
        UserSubscribe.user_id == telegram_id,
        UserSubscribe.subscribe == sub_id).update(
            {'status': subscribed}, synchronize_session='fetch')
    if not updated:
        db_session.add(UserSubscribe(user_id=telegram_id, subscribe=sub_id,
                                     status=subscribed))
    db_session.commit()
    logger.info(f'Пользователь {telegram_id}: подписка {sub_kind} = '
                f'{subscribed}')


def get_send_time(telegram_id: int) -> None:
    """Получить время рассылки для пользователя"""
    check = db_session.query(UserSendTime).filter(
        UserSendTime.user_id == telegram_id).all()
    if not check:
        return 'не установлено'
    else:
        return check[0].time


def create_update_send_time(telegram_id: int, time: str) -> None:
    """Запись о времени рассылки для пользователя"""
    check = db_session.query(UserSendTime).filter(
        UserSendTime.user_id == telegram_id).all()
    if not check:
        new_note = UserSendTime(user_id=telegram_id,
                                time=time
                                )
        db_session.add(new_note)
        db_session.commit()
    else:
        db_session.query(UserSendTime).filter(
            UserSendTime.user_id == telegram_id).update(
                {"time": time}, synchronize_session='fetch')
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


def delete_birthday_note(id: int, telegram_id: int) -> None:
    """Удаление записи о дне рождения.
    Удалить можно только свою запись."""
    check = db_session.query(Birthday).filter(
        Birthday.id == id).all()
    if not check:
        raise ValueError('Нет такой записи')
    if check[0].owner_id != telegram_id:
        raise PermissionError('Запись принадлежит другому пользователю')
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
            Birthday.owner_id == telegram_id
            ).order_by(Birthday.id).all()


def split_by_lines(lines: list[str], limit: int = 4096) -> list[str]:
    """Склеить строки в сообщения не длиннее limit (лимит Telegram)."""
    messages = []
    current = ''
    for line in lines:
        if current and len(current) + 1 + len(line) > limit:
            messages.append(current)
            current = line
        else:
            current = f'{current}\n{line}' if current else line
    messages.append(current)
    return messages
