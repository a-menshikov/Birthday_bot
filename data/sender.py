import asyncio
import logging

from aiogram.utils.exceptions import (BadRequest, RetryAfter,
                                      TelegramAPIError, Unauthorized)

from loader import bot

logger = logging.getLogger(__name__)

# Паузы между попытками, секунды. Часть соединений до api.telegram.org
# виснет на TLS-рукопожатии, следующая попытка обычно проходит.
RETRY_PAUSES = (3, 7, 10, 15, 25)


async def send_message_with_retry(chat_id, text, **kwargs):
    """bot.send_message с повторами при сбоях сети и Telegram.

    Каждая неудачная попытка пишется в лог с причиной. Отказ, который
    повтор не исправит (бот заблокирован, чат не найден, ошибка в разметке),
    и последняя неудачная попытка пробрасываются наружу, как у send_message.
    """
    attempts = len(RETRY_PAUSES) + 1
    for attempt in range(1, attempts + 1):
        try:
            return await bot.send_message(chat_id, text, **kwargs)
        except (TelegramAPIError, asyncio.TimeoutError) as error:
            logger.warning(f'Сообщение для {chat_id}, попытка {attempt} '
                           f'из {attempts}: {error!r}')
            if isinstance(error, (BadRequest, Unauthorized)):
                raise
            if attempt == attempts:
                raise
            pause = RETRY_PAUSES[attempt - 1]
            if isinstance(error, RetryAfter):
                pause = max(pause, error.timeout)
            await asyncio.sleep(pause)
