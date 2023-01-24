from aiogram import types
from aiogram.dispatcher import Dispatcher, FSMContext
from data.services import create_new_user, is_user_exist_in_base
from keyboards import (add_new_note, cancel_button, canсel_keyboard,
                       main_menu_keyboard, menu_button, menu_reply_keyboard,
                       reg_button, reg_keyboard)
from states.states import NewBirthdayStates


async def starter(message: types.Message):
    """Ответы на команды start и help"""
    telegram_id = message.from_user.id
    checker = is_user_exist_in_base(telegram_id)
    if checker:
        await message.answer("Привет. Этот бот умеет напоминать о ДР",
                             reply_markup=main_menu_keyboard())
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
                             reply_markup=main_menu_keyboard())
    else:
        create_new_user(telegram_id)
        await message.answer("Welcome. Полный функционал доступен."
                             " Воспользуйтесь меню",
                             reply_markup=main_menu_keyboard())


async def menu_sendler(message: types.Message):
    await message.answer("Вот такое щаз меню",
                         reply_markup=menu_reply_keyboard())


async def new_birthday(message: types.Message):
    """Добавление новой записи о дне рождения."""
    await NewBirthdayStates.name.set()
    await message.answer("Введиме имя. Лимит 200 символов",
                         reply_markup=canсel_keyboard())


async def name_input(message: types.Message, state: FSMContext):
    """Ввод имени для новой записи о дне рождения."""
    async with state.proxy() as data:
        data['name'] = message.text
    await NewBirthdayStates.next()
    await message.answer("Введите дату рождения в формате ДД.ММ.ГГГГ",
                         reply_markup=canсel_keyboard())


async def birth_date_input(message: types.Message, state: FSMContext):
    """Ввод даты рождения для новой записи о дне рождения."""
    async with state.proxy() as data:
        data['birth_date'] = message.text
    await NewBirthdayStates.next()
    await message.answer("Введите комментарий к записи.",
                         reply_markup=canсel_keyboard())


async def comment_input(message: types.Message, state: FSMContext):
    """Ввод коммента для новой записи о дне рождения."""
    async with state.proxy() as data:
        data['comment'] = message.text
    async with state.proxy() as data:
        # TODO дописать запись в базу
        await message.answer(data, reply_markup=menu_reply_keyboard())
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


def register_user_handlers(dp: Dispatcher):
    dp.register_message_handler(starter, commands=["start", "help"])
    dp.register_message_handler(registration, text=reg_button)
    dp.register_message_handler(menu_sendler, text=menu_button)
    dp.register_message_handler(cancel_add_note, text=cancel_button, state='*')
    dp.register_message_handler(new_birthday, text=add_new_note, state=None)
    dp.register_message_handler(name_input, state=NewBirthdayStates.name)
    dp.register_message_handler(birth_date_input,
                                state=NewBirthdayStates.birth_date)
    dp.register_message_handler(comment_input, state=NewBirthdayStates.comment)
    dp.register_message_handler(starter, commands=["start", "help"])
