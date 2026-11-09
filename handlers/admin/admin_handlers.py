from aiogram import types
from aiogram.dispatcher import Dispatcher
from aiogram.utils.exceptions import TelegramAPIError

from data.services import collect_admin_stats, is_admin
from handlers.other.other_handlers import unknown_message
from loader import bot


async def describe_user(telegram_id: int) -> str:
    """Ник или имя пользователя из Telegram, при сбое — только id."""
    try:
        chat = await bot.get_chat(telegram_id)
    except TelegramAPIError:
        return str(telegram_id)
    if chat.username:
        return f'@{chat.username} ({telegram_id})'
    name = ' '.join(part for part in (chat.first_name, chat.last_name) if part)
    return f'{name or "без имени"} ({telegram_id})'


async def stats(message: types.Message):
    """Статистика бота; для всех, кроме админа, команды как будто нет."""
    if not is_admin(message.from_user.id):
        await unknown_message(message)
        return
    data = collect_admin_stats()
    send_times = ', '.join(f'{time} — {count}' for time, count
                           in sorted(data['send_times'].items()))
    cf_file = (f"файл от {data['cf_file_date']:%d.%m.%Y}"
               if data['cf_file_date'] else 'файла нет')
    lines = [
        'Статистика бота',
        f"Пользователей: {data['users']}, получают рассылку: "
        f"{data['receiving']}",
        f"Личных записей: {data['notes']} у {data['note_owners']} "
        f"пользователей",
        f"ЦФ: {data['cf_people']} человек, подписчиков "
        f"{data['cf_subscribers']}, {cf_file}",
        f'Время рассылки: {send_times}',
    ]
    if data['without_subs']:
        names = [await describe_user(user_id)
                 for user_id in data['without_subs']]
        lines.append(f"Без подписок ({len(names)}): {', '.join(names)}")
    await message.answer('\n'.join(lines))


def register_admin_handlers(dp: Dispatcher):
    dp.register_message_handler(stats, commands=['stats'])
