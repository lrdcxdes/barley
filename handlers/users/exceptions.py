from aiogram.types import Update
from aiogram.utils.exceptions import (TelegramAPIError,
                                      MessageNotModified,
                                      CantParseEntities, BotBlocked)
import logging

from keyboard.jobs import report_kb


async def errors_handler(update: Update, exception):
    if isinstance(exception, MessageNotModified):
        return True

    if isinstance(exception, CantParseEntities):
        return True

    if isinstance(exception, BotBlocked):
        return True

    if isinstance(exception, TelegramAPIError):
        return True

    logging.exception(f'{exception}\n{update}')

    try:
        return await update.message.reply(text=f'Ошибка ❌',
                                          disable_notification=True,
                                          reply_markup=report_kb)
    except AttributeError:
        return await update.callback_query.answer(text=f'Ошибка ❌', show_alert=False)
