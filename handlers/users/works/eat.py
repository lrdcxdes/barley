from aiogram.types import Message


async def eats_handler(message: Message):
    return await message.reply(f'😷 Функция была убрана!')
