from aiogram.types import Message

from keyboard.countries import join_to_country_kb
from utils.countries import Country
from utils.main.cash import get_cash, to_str
from utils.main.db import sql


async def leave_from_country_handler(message: Message):
    country = Country.get_by_user(user_id=message.from_user.id)
    if country is None:
        return await message.reply('😐 Вы живёте на безлюдном острове.\n',
                                   reply_markup=join_to_country_kb())
    elif country.owner != message.from_user.id:
        return await message.reply('😐 Вы не являетесь президентом этой страны.')

    country.editmany(last_owner=message.from_user.id,
                     owner=None)

    return await message.reply(f'⛔ Вы ушли с поста президента страны {country.full_name}')


async def get_country_handler(message: Message):
    country = Country.get_by_user(user_id=message.from_user.id)
    if country is None:
        return await message.reply('😐 Вы живёте на безлюдном острове.\n',
                                   reply_markup=join_to_country_kb())
    elif country.owner is not None:
        return await message.reply(f'😐 У страны {country.full_name} уже есть президент!')

    country.editmany(owner=message.from_user.id)

    return await message.reply(f'✅ Вы приняли пост президента страны {country.full_name}!')


async def snyat_budget_country(message: Message):
    country = Country.get_by_user(user_id=message.from_user.id)
    if country is None:
        return await message.reply('😐 Вы живёте на безлюдном острове.\n',
                                   reply_markup=join_to_country_kb())
    elif country.owner != message.from_user.id:
        return await message.reply('😐 Вы не являетесь президентом этой страны.')\

    try:
        arg = get_cash(message.text.split()[2]) if message.text.split()[2].lower() not in ['всё', 'все'] else \
            country.balance
    except:
        return await message.reply('🤔 Неверно введена сумма для снятия с баланса страны!')

    if arg <= 0:
        return await message.reply('⛔ Сумма для снятия должна быть больше 0!')

    elif arg > country.balance:
        return await message.reply('⛔ На балансе страны недостаточно средств!')

    country.editmany(balance=country.balance - arg)
    sql.execute(f'UPDATE users SET balance = balance + {arg} WHERE id = {message.from_user.id}',
                True, False)
    return await message.reply(f'💸 Вы сняли {to_str(arg)} с баланса страны {country.full_name}!')


async def give_budget_country(message: Message):
    country = Country.get_by_user(user_id=message.from_user.id)
    if country is None:
        return await message.reply('😐 Вы живёте на безлюдном острове.\n',
                                   reply_markup=join_to_country_kb())
    elif country.owner != message.from_user.id:
        return await message.reply('😐 Вы не являетесь президентом этой страны.')
    try:
        bal =  sql.execute(f'SELECT balance FROM users WHERE id = {message.from_user.id}',
                           False, True)[0][0]
        arg = get_cash(message.text.split()[2]) if message.text.split()[2].lower() not in ['всё', 'все'] else \
        bal
                
    except:
        return await message.reply('🤔 Неверно введена сумма для пополнения баланса страны!')

    if arg <= 0:
        return await message.reply('⛔ Сумма для пополнения должна быть больше 0!')

    elif arg > bal:
        return await message.reply('⛔ На балансе недостаточно средств!')

    country.editmany(balance=country.balance + arg)
    sql.execute(f'UPDATE users SET balance = balance - {arg} WHERE id = {message.from_user.id}',
                True, False)
    return await message.reply(f'💸 Вы пополнили баланс страны {country.full_name} на +{to_str(arg)}!')
