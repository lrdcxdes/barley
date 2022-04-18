import random

from aiogram.types import Message

import config
from utils.main.bitcoin import Bitcoin, bitcoins, to_usd
from keyboard.generate import buy_ferm_kb, bitcoin_kb, show_balance_kb, show_ferm_kb
from utils.main.cash import get_cash, to_str
from utils.main.db import sql


async def bitcoin_handler(message: Message):
    arg = message.text.split()[1:] if not config.bot_name.lower() in message.text.split()[0].lower() else message.text.split()[2:]
    try:
        if message.text.split()[0].lower() == 'курс' or arg[0].lower() in ['курс', 'биткоин', 'биткоина']:
            return await message.reply('⭐ Текущий курс биткоина:\n'
                                       '➖➖➖➖➖➖➖➖➖➖➖➖➖\n'
                                       f'<b>1BTC⭐</b> = {to_str(to_usd(1))}')
    except:
        pass
    if len(arg) == 0 or arg[0].lower() not in ['внести', 'купить',
                                               'пополнить', 'курс', 'биткоин',
                                               'биткоина', 'продать', 'снять',
                                               'обменять']:
        return await ferma_handler(message)

    elif len(arg) < 2 and arg[0].lower() not in ['продать', 'снять', 'обменять']:
        return await message.reply('❌ Используйте: <code>Биткоин купить {кол-во}</code>')

    try:
        bitcoin = Bitcoin(owner=message.from_user.id)
    except:
        bitcoin = None

    if not bitcoin:
        return await message.reply('❌ У вас нет фермы!', buy_ferm_kb)

    elif arg[0].lower() in ['продать', 'снять', 'обменять']:
        try:
            if arg[1].isdigit():
                summ = get_cash(arg[1])
            else:
                raise Exception('123')
        except:
            summ = bitcoin.balance_
        if summ <= 0:
            return await message.reply('😴 Кол-во BTC меньше или равно нулю!')
        elif summ > bitcoin.balance_:
            return await message.reply('😴 Кол-во BTC больше чем баланс фермы!')

        now = config.bitcoin_price() - int(summ * 0.05)

        await config.set_bitcoin_price(now)

        user_summ = to_usd(summ)

        sql.executescript(f'UPDATE bitcoin SET balance = balance - {summ} WHERE id = {bitcoin.id};\n'
                          f'UPDATE users SET bank = bank + {user_summ} WHERE id = {message.from_user.id};',
                          True, False)

        await message.reply(f'✅ Вы успешно сняли {to_str(user_summ)} с биткоин фермы!')

        return
    else:
        try:
            xa = sql.execute(f'SELECT bank FROM users WHERE id = {message.from_user.id}', False, True)[0][0]
            summ = get_cash(arg[1]) if arg[1].lower() not in ['всё', 'все'] else int(xa / to_usd(1))
            if summ <= 0:
                raise Exception('123')
        except:
            return await message.reply('❌ Используйте: <code>Биткоин купить {кол-во}</code>')

        user_summ = to_usd(summ)

        if user_summ > xa:
            return await message.reply(f'❌ Недостаточно денег в банке! Нужно: {to_str(user_summ)}')

        sql.executescript(f'UPDATE bitcoin SET balance = balance + {summ} WHERE id = {bitcoin.id};\n'
                          f'UPDATE users SET bank = bank - {user_summ} WHERE id = {message.from_user.id};',
                          True, False)

        await message.reply(f'✅ Вы успешно приобрели {summ} биткоинов за {to_str(user_summ)}',
                            reply_markup=show_balance_kb)

        now = config.bitcoin_price() + int(summ * random.choice([0.01, 0.05, 0.04, 0.03, 0]))

        await config.set_bitcoin_price(now)

        return


async def videocards_handler(message: Message):
    arg = message.text.split()[1:] if not config.bot_name.lower() in message.text.split()[0].lower() else message.text.split()[2:]
    if len(arg) == 0 or arg[0].lower() not in ['внести', 'купить',
                                               'пополнить']:
        return await message.reply('❌ Используйте: <code>Видеокарты купить {кол-во}</code>')

    try:
        bitcoin = Bitcoin(owner=message.from_user.id)
    except:
        bitcoin = None

    if bitcoin is None:
        return await message.reply('❌ У вас нет фермы!', buy_ferm_kb)

    try:
        count = int(arg[1])
        if count <= 0:
            raise Exception('123')
    except:
        count = 1
    cc = bitcoin.videocards if bitcoin.videocards > 0 else 1

    summ = int((bitcoin.bitcoin.videoprice * count) * cc)

    if summ > sql.execute(f'SELECT balance FROM users WHERE id = {message.from_user.id}', False, True)[0][0]:
        return await message.reply(f'❌ Недостаточно денег на руках, нужно: {to_str(summ)}',
                                   reply_markup=show_balance_kb)

    sql.executescript(f'UPDATE bitcoin SET videocards = videocards + {count} WHERE id = {bitcoin.id};\n'
                      f'UPDATE users SET balance = balance - {summ} WHERE id = {message.from_user.id};',
                      True, False)

    return await message.reply(f'✅ Вы успешно приобрели {count} видеокарт(у) за {to_str(summ)}',
                               reply_markup=show_ferm_kb)


async def ferma_handler(message: Message):
    try:
        bitcoin = Bitcoin(owner=message.from_user.id)
    except:
        bitcoin = None

    arg = message.text.split()[1:] if not config.bot_name.lower() in message.text.split()[0].lower() else message.text.split()[2:]
    if (len(arg) == 0 and bitcoin is None) or (len(arg) > 0 and arg[0].lower() in ['список', 'все', 'инфо']):
        text = '🖥️ Список биткоин-ферм:\n<i>Номер. Название - цена - доход - налог</i>\n\n'
        for index, i in bitcoins.items():
            i = i()
            text += f'{index}. <b>{i.name}</b> - {to_str(i.price)} - <code>{i.doxod}BTC</code> - <code' \
                    f'>{i.nalog}</code>\n'
        return await message.reply(text=text, reply_markup=buy_ferm_kb)

    elif len(arg) > 0 and arg[0].lower() == 'купить':
        try:
            index = int(arg[1])
            if index < 1 or index > len(bitcoins):
                raise Exception('123')
        except:
            return await message.reply('❌ Неверный номер фермы!')
        xa = sql.execute(f'SELECT balance FROM users WHERE id = {message.from_user.id}', False, True)[0][0]
        b = bitcoins[index]()
        x = b.price
        if x > xa:
            return await message.reply(f'❌ Недостаточно денег в банке! Нужно: {to_str(x)}',
                                       reply_markup=show_balance_kb)
        Bitcoin.create(message.from_user.id, index)
        sql.execute(f'UPDATE users SET balance = balance - {b.price} WHERE id = {message.from_user.id}',
                    True, False)
        return await message.reply(f'✅ Вы успешно приобрели ферму <b>{b.name}</b> за {to_str(x)}',
                                   reply_markup=show_ferm_kb)

    elif bitcoin is None:
        return await message.reply('❌ У вас нет фермы')
    elif len(arg) == 0 and bitcoin:
        return await message.reply(text=bitcoin.text, reply_markup=bitcoin_kb)
    elif len(arg) < 1:
        return await message.reply('❌ Используйте: <code>Ферма [купить|продать|снять|налог] *{сумма}</code>')

    elif arg[0].lower() == 'продать':
        price = bitcoin.sell()
        if price > 0:
            sql.execute(f'UPDATE users SET balance = balance + {price} WHERE id = {message.from_user.id}',
                        True, False)
        return await message.reply(f'✅ Вы успешно продали ферму за {to_str(price)}')

    elif arg[0].lower() in ['снять', 'вывести', 'доход',
                            'выложить', 'забрать', 'продать']:
        try:
            if arg[1].isdigit():
                summ = get_cash(arg[1])
            else:
                raise Exception('123')
        except:
            summ = bitcoin.balance_
        if summ <= 0:
            return await message.reply('😴 Кол-во BTC меньше или равно нулю!')
        elif summ > bitcoin.balance_:
            return await message.reply('😴 Кол-во BTC больше чем баланс фермы!')

        now = config.bitcoin_price() - int(summ * 0.05)

        await config.set_bitcoin_price(now)

        user_summ = to_usd(summ)

        sql.executescript(f'UPDATE bitcoin SET balance = balance - {summ} WHERE id = {bitcoin.id};\n'
                          f'UPDATE users SET bank = bank + {user_summ} WHERE id = {message.from_user.id};',
                          True, False)

        await message.reply(f'✅ Вы успешно сняли {to_str(user_summ)} с биткоин фермы!')

        return

    elif arg[0].lower() in ['оплатить', 'налог', 'налоги']:
        try:
            if arg[1].isdigit():
                summ = get_cash(arg[1])
            else:
                raise Exception('123')
        except:
            summ = bitcoin.nalog

        if summ <= 0:
            return await message.reply('😴 Сумма меньше или равна нулю!')
        elif summ > bitcoin.nalog:
            return await message.reply('😴 Сумма больше чем налог фермы!')
        elif sql.execute(f'SELECT bank FROM users WHERE id = {message.from_user.id}', False, True)[0][0] < summ:
            return await message.reply('❌ Недостаточно денег в банке '
                                       f'для оплаты налогов, нужно: {to_str(bitcoin.nalog)}',
                                       reply_markup=show_balance_kb)
        sql.executescript(f'UPDATE bitcoin SET nalog = nalog - {summ} WHERE id = {bitcoin.id};\n'
                          f'UPDATE users SET bank = bank - {summ} WHERE id = {message.from_user.id};',
                          True, False)

        return await message.reply(f'✅ Вы успешно оплатили налог с биткоин фермы!',
                                   reply_markup=show_ferm_kb)
    else:
        return await message.reply('❌ Используйте: <code>Ферма [купить|продать|снять|налог] *{сумма}</code>')
