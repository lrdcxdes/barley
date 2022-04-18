import time

from aiogram.types import Message

from config import bot_name
from utils.countries import Country


async def wars_handler(message: Message):
    country = Country.get_by_user(message.from_user.id)
    if country.owner != message.from_user.id:
        return await message.reply('😐 Вы не президент страны!')

    elif country.war is not None:
        return await message.reply(f'🤔 В данный момент идёт война против {country.war.full_name}!')

    arg = message.text.split()[2:] if not bot_name.lower() in message.text.split()[0].lower() else message.text.split()[3:]

    try:
        country2 = Country.find_country(arg[0].lower())
        if country2 is None or country2.id == country.id:
            raise Exception('123')
    except:
        return await message.reply('🤔 Неверно указана страна, которой вы хотите обьявить войну!')

    if country2.war:
        return await message.reply('😐 В стране с которой вы хотите воевать и так сейчас идёт война против '
                                   f'{country2.war.full_name}!')
    elif country.soyuz == country2:
        return await message.reply('😐 Вы не можете обьявить войну своему союзнику!')

    country.editmany(war=country2.id, attr=False,
                     war_time=time.time())
    country.war_time = time.time()
    country.war = country2
    country2.editmany(war=country.id, attr=False,
                      war_time=time.time())
    country2.war_time = time.time()
    country2.war = country
    return await message.reply('🤔 Вы обьявили войну против страны {}!'.format(country2.full_name))


async def cancel_wars_handler(message: Message):
    country = Country.get_by_user(message.from_user.id)
    if country.owner != message.from_user.id:
        return await message.reply('😐 Вы не президент страны!')

    elif country.war is None:
        return await message.reply('🤔 Вы не обьявили никому войну!')

    country.edit('war', None, False)
    country.war.edit('war', None, False)
    await message.reply(f'🤔 Вы отменили войну против {country.war.full_name}!')

    country.war.war = None
    country.war = None
