from aiogram import types
from aiogram.dispatcher import Dispatcher, FSMContext
from data.services import (all_sub_check, create_new_birthday_note,
                           create_new_user, get_today_birthdays_cf,
                           get_today_birthdays_private, get_user_base_id,
                           is_user_exist_in_base, view_users_birthday_notes)
from keyboards import (add_new_note, cancel_button, canсel_keyboard,
                       in_main_menu, menu_reply_keyboard, my_birthdays_button,
                       reg_button, reg_keyboard, sub_keyboard, subscribes,
                       today_birthday)
from loader import today_full_date
from states.states import NewBirthdayStates

from .validators import validate_birthday, validate_comment, validate_name


async def starter(message: types.Message):
    """Ответы на команды start и help"""
    telegram_id = message.from_user.id
    checker = is_user_exist_in_base(telegram_id)
    if checker:
        await message.answer("Привет. Этот бот умеет напоминать о ДР",
                             reply_markup=menu_reply_keyboard(telegram_id))
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
                             reply_markup=menu_reply_keyboard(telegram_id))
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
                             reply_markup=menu_reply_keyboard(telegram_id))
    else:
        create_new_user(telegram_id)
        await message.answer("Welcome. Полный функционал доступен."
                             " Воспользуйтесь меню",
                             reply_markup=menu_reply_keyboard(telegram_id))


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

    await NewBirthdayStates.next()
    await message.answer("Введите комментарий к записи. Лимит 200 символов.",
                         reply_markup=canсel_keyboard())


async def comment_input(message: types.Message, state: FSMContext):
    """Ввод коммента для новой записи о дне рождения."""
    comment = message.text
    telegram_id = message.from_user.id
    if not validate_comment(comment):
        await message.answer(
            'Что то не так с введенным комментарием.\n'
            'Текст должен состоять из цифр или '
            'букв русского/латинского алфавитов '
            'и быть не более 200 символов.'
        )
        return
    async with state.proxy() as data:
        data['comment'] = message.text
        data['owner_id'] = get_user_base_id(telegram_id)
        create_new_birthday_note(data)
        await message.answer("Запись создана",
                             reply_markup=menu_reply_keyboard(telegram_id))
    await state.finish()


async def cancel_add_note(message: types.Message, state: FSMContext):
    """Отмена добавления новой записи о дне рождения."""
    current_state = await state.get_state()
    telegram_id = message.from_user.id
    if current_state is not None:
        await state.finish()
        await message.answer('Операция отменена',
                             reply_markup=menu_reply_keyboard(telegram_id))
    else:
        await message.answer('Так ведь нечего отменять',
                             reply_markup=menu_reply_keyboard(telegram_id))


async def my_birthdays(message: types.Message):
    """Вывод информации о ДР_записях пользователя."""
    telegram_id = message.from_user.id
    notes = view_users_birthday_notes(telegram_id)
    await message.answer(notes,
                         reply_markup=menu_reply_keyboard(telegram_id))


async def today_birthdays(message: types.Message):
    """Вывод информации о ДР в подписках пользователя сегодня."""
    telegram_id = message.from_user.id
    subscribe_status = all_sub_check(telegram_id)
    base_message = f'Дата: {today_full_date}\n\n'
    if subscribe_status['private']:
        private = get_today_birthdays_private(telegram_id)
        base_message += 'В ЛИЧНЫХ ЗАПИСЯХ:\n\n'
        if private:
            for i in private:
                add_message = (f'{i[0]}\n'
                               f'{i[1]}\n'
                               f'{i[2]}\n\n'
                               )
                base_message += add_message
        else:
            base_message += 'Сегодня нет дней рождения\n\n'
    if subscribe_status['cf']:
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
        else:
            base_message += 'Сегодня нет дней рождения\n'
    await message.answer(base_message,
                         reply_markup=menu_reply_keyboard(telegram_id),
                         )


def register_user_handlers(dp: Dispatcher):
    dp.register_message_handler(starter, commands=["start", "help"])
    dp.register_message_handler(registration, text=reg_button)
    dp.register_message_handler(main_menu, text=in_main_menu)
    dp.register_message_handler(my_birthdays, text=my_birthdays_button)
    dp.register_message_handler(today_birthdays, text=today_birthday)
    dp.register_message_handler(cancel_add_note, text=cancel_button, state='*')
    dp.register_message_handler(my_subscribes, text=subscribes)
    dp.register_message_handler(new_birthday, text=add_new_note, state=None)
    dp.register_message_handler(name_input, state=NewBirthdayStates.name)
    dp.register_message_handler(birth_date_input,
                                state=NewBirthdayStates.birth_date)
    dp.register_message_handler(comment_input, state=NewBirthdayStates.comment)
