from aiogram import types
from aiogram.dispatcher import Dispatcher, FSMContext

from data.services import (all_sub_check, create_new_birthday_note,
                           create_new_user, create_update_send_time,
                           delete_birthday_note, get_send_time,
                           is_user_exist_in_base, make_future_bd_message,
                           make_today_bd_message, view_users_birthday_notes)
from keyboards import (add_new_note, cancel_button, canсel_keyboard,
                       future_birthday, in_main_menu, menu_reply_keyboard,
                       my_birthdays_button, reg_button, reg_keyboard,
                       sub_keyboard, time_1, time_2, time_3, time_4, time_5,
                       time_6, time_reply_keyboard, time_setting,
                       today_birthday)
from states.states import NewBirthdayStates

from .validators import validate_birthday, validate_name


async def starter(message: types.Message):
    """Ответы на команды start и help"""
    telegram_id = message.from_user.id
    checker = is_user_exist_in_base(telegram_id)
    if checker:
        await message.answer("Привет. Этот бот умеет напоминать о ДР",
                             reply_markup=menu_reply_keyboard())
    else:
        await message.answer("Привет. Этот бот умеет напоминать о ДР."
                             "Жми кнопку и начнём!",
                             reply_markup=reg_keyboard())


async def main_menu(message: types.Message):
    """В главное меню."""
    telegram_id = message.from_user.id
    checker = is_user_exist_in_base(telegram_id)
    if checker:
        await message.answer("Меню:",
                             reply_markup=menu_reply_keyboard())
    else:
        await message.answer("Привет. Этот бот умеет напоминать о ДР."
                             "Жми кнопку и начнём!",
                             reply_markup=reg_keyboard())


async def registration(message: types.Message):
    """Регистрация нового пользователя."""
    telegram_id = message.from_user.id
    checker = is_user_exist_in_base(telegram_id)
    if checker:
        await message.answer("Вы уже зарегистрированы. Воспользуйтесь меню",
                             reply_markup=menu_reply_keyboard())
    else:
        create_new_user(telegram_id)
        await message.answer("Welcome. Полный функционал доступен."
                             " Воспользуйтесь меню",
                             reply_markup=menu_reply_keyboard())


async def my_subscribes(message: types.Message):
    """Переход в меню подписок."""
    telegram_id = message.from_user.id
    sub_status = all_sub_check(telegram_id)
    await message.answer("Ваши подписки.",
                         reply_markup=sub_keyboard(sub_status))


async def new_birthday(message: types.Message):
    """Добавление новой записи о дне рождения."""
    await NewBirthdayStates.name.set()
    await message.answer("Введиме имя. Лимит 200 символов.",
                         reply_markup=canсel_keyboard())


async def name_input(message: types.Message, state: FSMContext):
    """Ввод имени для новой записи о дне рождения."""
    name = message.text
    if not validate_name(name):
        await message.answer(
            'Что то не так с введенным именем.\n'
            'Имя должно состоять из цифр или '
            'букв русского/латинского алфавитов '
            'и быть не более 200 символов.'
        )
        return
    async with state.proxy() as data:
        data['name'] = message.text
    await NewBirthdayStates.next()
    await message.answer("Введите дату рождения в формате ДД.ММ",
                         reply_markup=canсel_keyboard())


async def birth_date_input(message: types.Message, state: FSMContext):
    """Ввод даты рождения для новой записи о дне рождения."""
    birthday = message.text
    telegram_id = message.from_user.id
    if not validate_birthday(birthday):
        await message.answer(
            'Что то не так с введенной датой.\n'
            'Сообщение дожно быть в формате ДД.ММ '
            '(например 13.04 или 29.02) и быть реальной датой.'
        )
        return
    day, month = map(int, message.text.split('.'))
    async with state.proxy() as data:
        data['day_of_birth'] = day
        data['month_of_birth'] = month
        data['row_birth_date'] = birthday

    async with state.proxy() as data:
        data['comment'] = message.text
        data['owner_id'] = telegram_id
        create_new_birthday_note(data)
        await message.answer("Запись создана",
                             reply_markup=menu_reply_keyboard())
    await state.finish()


async def cancel_add_note(message: types.Message, state: FSMContext):
    """Отмена добавления новой записи о дне рождения."""
    current_state = await state.get_state()
    if current_state is not None:
        await state.finish()
        await message.answer('Операция отменена',
                             reply_markup=menu_reply_keyboard())
    else:
        await message.answer('Так ведь нечего отменять',
                             reply_markup=menu_reply_keyboard())


async def my_birthdays(message: types.Message):
    """Вывод информации о ДР_записях пользователя."""
    telegram_id = message.from_user.id
    notes = view_users_birthday_notes(telegram_id)
    if notes:
        text = ''
        for i in notes:
            text += f'{i[0]}.  {i[1]},  {i[2]} \n'
        text += ('\n Чтобы удалить запись отправь боту '
                 'сообщение формата "Удалить Х", где Х '
                 'номер записи в этом списке.')
        await message.answer(text)
    else:
        text = ('Список пустой')
        await message.answer(text,
                             reply_markup=menu_reply_keyboard())


async def today_birthdays(message: types.Message):
    """Вывод информации о ДР в подписках пользователя сегодня."""
    telegram_id = message.from_user.id
    base_message, empty = make_today_bd_message(telegram_id)
    await message.answer(base_message,
                         reply_markup=menu_reply_keyboard(),
                         )


async def future_birthdays(message: types.Message):
    """Вывод информации о ДР в подписках пользователя в ближайшие дни."""
    telegram_id = message.from_user.id
    base_message, empty = make_future_bd_message(telegram_id)
    await message.answer(base_message,
                         reply_markup=menu_reply_keyboard(),
                         )


async def set_time_menu(message: types.Message):
    """Переход в меню настройки времени рассылки."""
    telegram_id = message.from_user.id
    now_time = get_send_time(telegram_id)
    base_message = (f'Текущее время рассылки: {now_time}.\n'
                    f'Часовой пояс GMT+3 (Московский).')
    await message.answer(base_message,
                         reply_markup=time_reply_keyboard(),
                         )


async def set_time_send(message: types.Message):
    """Установка времени рассылки."""
    telegram_id = message.from_user.id
    create_update_send_time(telegram_id, message.text)
    base_message = (f'Установлено время рассылки {message.text}.\n'
                    f'Часовой пояс GMT+3 (Московский).')
    await message.answer(base_message,
                         reply_markup=menu_reply_keyboard(),
                         )


async def delete_bd_note(message: types.Message):
    """Удалить запись о др."""
    try:
        note_id = int(message.text.split()[1])
        delete_birthday_note(note_id)
        await message.answer('Запись удалена',
                             reply_markup=menu_reply_keyboard())
    except IndexError:
        await message.answer('Запрос не соответствует формату "Удалить Х"',
                             reply_markup=menu_reply_keyboard())
    except ValueError:
        await message.answer('Запись не существует или '
                             'принадлежит другому пользователю',
                             reply_markup=menu_reply_keyboard())


def register_user_handlers(dp: Dispatcher):
    dp.register_message_handler(starter, commands=["start", "help"])
    dp.register_message_handler(registration, text=reg_button)
    dp.register_message_handler(main_menu, text=in_main_menu)
    dp.register_message_handler(my_birthdays, text=my_birthdays_button)
    dp.register_message_handler(today_birthdays, text=today_birthday)
    dp.register_message_handler(future_birthdays, text=future_birthday)
    dp.register_message_handler(set_time_menu, text=time_setting)
    dp.register_message_handler(set_time_send, text=[time_1, time_2,
                                                     time_3, time_4,
                                                     time_5, time_6])
    dp.register_message_handler(cancel_add_note, text=cancel_button, state='*')
    dp.register_message_handler(new_birthday, text=add_new_note, state=None)
    dp.register_message_handler(name_input, state=NewBirthdayStates.name)
    dp.register_message_handler(birth_date_input,
                                state=NewBirthdayStates.birth_date)
    dp.register_message_handler(delete_bd_note,
                                text_startswith=['Удалить', 'удалить'])
