from aiogram.dispatcher.filters.state import State, StatesGroup


class NewBirthdayStates(StatesGroup):
    """Машина состояний новой записи о дне рождения."""
    name = State()
    birth_date = State()
    comment = State()
