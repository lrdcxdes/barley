from aiogram.types import Message

from config import bot_name
from keyboard.countries import join_to_country_kb, country_kb, get_country_kb
from utils.countries import Country


async def my_country_handler(message: Message):
    country = Country.get_by_user(user_id=message.from_user.id)
    if country is None:
        return await message.reply('😐 Вы живёте на безлюдном острове.\n',
                                   reply_markup=join_to_country_kb())
    text = country.text
    return await message.reply('🌍 Вы живёте в этой стране:\n\n{}'.format(text), reply_markup=None
                               if country.owner != message.from_user.id else country_kb if country.owner
                               else get_country_kb(country.name))


async def join_country_handler(message: Message):
    arg = message.text.split() if not bot_name.lower() in message.text.split()[0].lower() else message.text.split()[1:]

    country = Country.get_by_user(user_id=message.from_user.id)
    if country is not None:
        return await message.reply('😐 Вы уже и так в какой-то стране!')

    country = Country.find_country(' '.join(arg[3:]).lower())
    if country is None:
        return await message.reply('⛔ Такой страны не существует!')

    country.add_user(message.from_user.id)
    return await message.reply(text=f'✅ Вы получили гражданство в стране {country.full_name}!')


async def leave_country_handler(message: Message):
    country = Country.get_by_user(user_id=message.from_user.id)
    if country is None:
        return await message.reply('😐 Вы живёте на безлюдном острове.\n',
                                   reply_markup=join_to_country_kb())
    elif message.from_user.id == country.owner:
        return await message.reply('⛔ Вы не можете покинуть свою страну ибо вы президент!')
    elif country.war:
        return await message.reply('⛔ Вы не можете покинуть страну ибо в ней война!')
    country.del_user(message.from_user.id)
    return await message.reply('🌍 Вы покинули страну {}'.format(country.full_name))
