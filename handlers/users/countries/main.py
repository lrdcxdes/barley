import re

from aiogram.types import Message

from config import bot_name
from keyboard.countries import countries_main_kb, country_kb, join_to_country_kb, get_country_kb
from utils.countries import Country, countries, set_country, country_creation_price
from utils.main.cash import to_str
from utils.main.db import sql


async def countries_handler(message: Message):
    arg = message.text.split()[1:] if not bot_name.lower() in message.text.split()[0].lower() else message.text.split()[2:]
    if len(arg) == 0 or arg[0].lower() == 'список':
        text = '🏴‍☠️ Государства (по територии) (топ 5):\n\n'
        for index, country in Country.get_top(10):
            text += f'{index}. {country.full_name} (<code>{country.territory} км²</code>) - {country.owner_link}\n'
        text += '\n\nВведите: <code>Страна {название/номер}</code> чтобы получить информацию о стране.\n' \
                'Введите: <code>Страны список</code> чтобы получить список всех стран.'
        return await message.reply(text, reply_markup=countries_main_kb, disable_web_page_preview=True)
    elif len(arg) == 1:
        country = Country.find_country(arg[0])
        if country is None:
            return await message.reply('🚫 Страна не найдена.')
        return await message.reply(country.text, reply_markup=join_to_country_kb(country.name) if country.owner !=
                                                                                               message.from_user.id
        else country_kb if country.owner is not None else get_country_kb(country.name))
    else:
        return await message.reply('🚫 Неверный аргумент.')


def is_flag_emoji(c):
    return "\U0001F1E6\U0001F1E8" <= c <= "\U0001F1FF\U0001F1FC" or c in ["\U0001F3F4\U000e0067\U000e0062\U000e0065"
                                                                          "\U000e006e\U000e0067\U000e007f",
                                                                          "\U0001F3F4\U000e0067\U000e0062\U000e0073"
                                                                          "\U000e0063\U000e0074\U000e007f",
                                                                          "\U0001F3F4\U000e0067\U000e0062\U000e0077"
                                                                          "\U000e006c\U000e0073\U000e007f"]


async def country_create_handler(message: Message):
    country = Country.get_by_user(user_id=message.from_user.id)
    if country is not None:
        return await message.reply('😐 Вы уже и так в какой-то стране!\n'
                                   'Введите: <code>Выйти из страны</code> чтобы выйти из страны.')
    arg = message.text.split()[2:]
    if len(arg) == 0:
        return await message.reply('🚫 Вы не ввели название страны! <code>(Пример: Расея🏳️‍🌈)</code>')

    msg = ' '.join(arg)
    name = re.sub(r'[^a-zA-Zа-яА-Я0-9 ]', '', msg).capitalize()
    if len(name) < 4:
        return await message.reply('🚫 Название страны должно быть больше 4 символов.')
    elif len(name) > 20:
        return await message.reply('🚫 Название страны должно быть меньше 20 символов.')
    elif name.count(' ') > 2:
        return await message.reply('🚫 Название страны может содержать только 2 пробела.')
    elif name.lower() in [country.name.lower() for country in countries().values()]:
        return await message.reply('🚫 Страна с таким названием уже существует.')

    try:
        emoji = None
        for index, char in enumerate(msg):
            if index+1 >= len(msg):
                break
            if is_flag_emoji(msg[index:index+2]):
                emoji = msg[index:index+2]
                break
        if not emoji:
            return await message.reply('🚫 Вы не указали эмодзи страны.')
    except Exception as ex:
        print(ex)
        return await message.reply('🚫 Вы не указали эмодзи страны.')

    balance = sql.execute(f'SELECT balance FROM users WHERE id = {message.from_user.id}', False, True)[0][0]
    if balance < country_creation_price:
        return await message.reply(f'😐 У вас недостаточно средств для создания страны.\n'
                                   f'Нужно: {to_str(country_creation_price)} 💰')

    src = (None, name, emoji, 0, message.from_user.id, None, f'{message.from_user.id}', 0, None, '0,0,0,False', None,
           None)
    sql.insert_data([src], 'countries')
    sql.edit_data('id', message.from_user.id,
                  'balance', balance - country_creation_price)

    c = Country(sql.select_data(name, 'name', True, 'countries'))

    set_country(c.id, c)

    return await message.reply(f'😐 Вы успешно создали страну {c.full_name} за {to_str(country_creation_price)}')
