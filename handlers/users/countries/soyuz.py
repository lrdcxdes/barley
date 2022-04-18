from aiogram.types import Message

from config import bot_name
from utils.countries import Country


async def soyuz_handler(message: Message):
    arg = message.text.split()[2:] if not bot_name.lower() in message.text.split()[0].lower() else message.text.split()[3:]

    country = Country.get_by_user(message.from_user.id)
    if country.owner != message.from_user.id:
        return await message.reply('😐 Вы не президент страны!')

    elif country.soyuz is not None:
        return await message.reply(f'🤔 В данный момент вы в союзе с {country.soyuz.full_name}!')

    try:
        country2 = Country.find_country(arg[0].lower())
        if country2 is None or country2.id == country.id:
            raise Exception('123')
    except:
        return await message.reply('🤔 Неверно указана страна, с которой вы хотите союз!')

    country.edit('soyuz', country2.id, False)
    country.soyuz = country2
    country2.edit('soyuz', country.id, False)
    country2.soyuz = country

    return await message.reply('🤔 Вы создали союз со страной {}!'.format(country2.full_name))


async def cancel_soyuz_handler(message: Message):
    country = Country.get_by_user(message.from_user.id)
    if country.owner != message.from_user.id:
        return await message.reply('😐 Вы не президент страны!')

    elif country.soyuz is None:
        return await message.reply('🤔 Вы не обьявили никому союз!')

    country.edit('soyuz', None, False)
    country.soyuz.edit('soyuz', None, False)
    await message.reply(f'🤔 Вы отменили союз со страной {country.soyuz.full_name}!')

    country.soyuz.soyuz = None
    country.soyuz = None
