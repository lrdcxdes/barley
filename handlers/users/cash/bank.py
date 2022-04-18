import datetime
import time

from aiogram.types import Message

import config
from utils.logs import writelog
from utils.main.cash import to_str, get_cash
from utils.main.db import timetostr
from utils.main.users import User


async def bank_handler(message: Message):
    spliy = message.text.split() if not config.bot_name.lower() in message.text.split()[0].lower() else message.text.split()[1:]
    user = User(user=message.from_user)
    try:
        arg = abs(get_cash(spliy[2].lower().replace('всё', str(user.bank)).replace('все', str(user.bank)))) if spliy[
            1].lower() in ['снять', 'вывести', 'обналичить'] else abs(get_cash(
            spliy[2].lower().replace('всё', str(user.balance)).replace('все', str(user.balance))))
        if arg <= 0:
            raise Exception(123)
    except:
        return await message.reply(f'❌ Ошибка! Неверный аргумент, введите: <code>банк [снять|пополнить|вывести] {{ '
                                   f'сумма }}</code>')
    if spliy[1].lower() in ['положить', 'пополнить', 'внести']:
        if user.balance < arg:
            return await message.reply('💸 На руках недостаточно средств, чтобы пополнить такую сумму в банк!')
        user.editmany(balance=user.balance - arg, bank=user.bank + arg)
        await message.reply(f'✅ Вы пополнили баланс в банке на +{to_str(arg)}, текущий баланс в банке: '
                                   f'{to_str(user.bank)}')
        await writelog(message.from_user.id, f'Банк +{to_str(arg)}')
        return
    elif spliy[1].lower() in ['снять', 'вывести', 'обналичить']:
        if user.bank < arg:
            return await message.reply('💳 В банке недостаточно средств, чтобы снять средства!')
        user.editmany(balance=user.balance + arg, bank=user.bank - arg)
        await message.reply(f'✅ Вы сняли средства в размере {to_str(arg)} и теперь у вас на руках '
                                   f'{to_str(user.balance)}')
        await writelog(message.from_user.id, f'Банк -{to_str(arg)}')
        return
    elif spliy[1].lower() in ['кредит', 'взять', 'погасить']:
        return await credit_handler(message)
    else:
        return await message.reply(f'❌ Ошибка! Неверный аргумент, введите: <code>банк [снять|пополнить|вывести] {{ '
                                   f'сумма }}</code>')


async def credit_handler(message: Message):
    spliy = message.text.split()[1:]
    try:
        arg = abs(int(spliy[1].replace('$', '').replace('.', '').replace(',', '').replace(' ', '')))
        if arg <= 0:
            raise Exception(123)
    except:
        return await message.reply(f'❌ Ошибка! Неверный аргумент, введите: <code>Кредит [взять|погасить] {{ '
                                   f'сумма }}</code>')

    user = User(user=message.from_user)
    if spliy[0] == 'взять':
        if ((user.reg_date + datetime.timedelta(days=1)) - datetime.datetime.now()).total_seconds() > 1:
            xax = timetostr(int(((user.reg_date + datetime.timedelta(days=1) - datetime.datetime.now(

            )).total_seconds())))
            return await message.reply(f'⌚ Вам нужно отыграть ещё <code>{xax}</code> чтобы появилась возможность брать '
                                       f'кредит!')
        elif user.credit >= config.credit_limit:
            return await message.reply(f'❗ Вы достигли лимита кредита {to_str(user.credit)}')
        elif arg > config.credit_limit or arg > config.credit_limit - user.credit:
            return await message.reply(f'❗ Сумма которая вам доступна'
                                       f' для взятия в кредит: {to_str(config.credit_limit - user.credit)}')
        user.editmany(credit_time=time.time(),
                      bank=user.bank + arg,
                      credit=user.credit + arg)
        await message.reply(f'💼 Вы взяли в кредит {to_str(arg)} под {config.credit_percent}%,'
                                   f' каждые 2 часа у вас будут сниматься деньги'
                                   f' с основных счетов если вы не выплатите кредит!')
        await writelog(message.from_user.id, f'Кредит +{to_str(arg)}')
        return
    else:
        if arg > user.credit:
            return await message.reply('❗ Сумма которую вы ввели для погашения больше чем у вас кредит.')
        elif arg > user.bank:
            return await message.reply('❗ Сумма в банке недостаточна для погашения кредита!')
        user.editmany(credit=user.credit - arg,
                      credit_time=time.time() if user.credit - arg > 0 else None,
                      bank=user.bank - arg)
        await message.reply(f'✅ Вы погасили кредит на -{to_str(arg)}, текущая сумма на кредитном счету: '
                                   f'{to_str(user.credit)}')
        await writelog(message.from_user.id, f'Кредит -{to_str(arg)}')
        return
