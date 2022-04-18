import random

from aiogram.types import Message

from config import uah_price, set_uah_price, bot_name
from keyboard.generate import show_balance_kb
from keyboard.cash import uah_kb, my_uah_kb
from utils.main.cash import get_cash, to_str
from utils.main.db import sql
from utils.main.euro import Uah, uah_to_usd


async def uah_handler(message: Message):
    arg = message.text.split()[1:] if not bot_name.lower() in message.text.split()[0].lower() else message.text.split()[2:]
    uah = Uah(owner=message.from_user.id)

    if len(arg) == 0 or arg[0].lower() in ['моя', 'мои', 'ми', 'мой']:
        return await message.reply(uah.text, reply_markup=uah_kb)
    elif arg[0].lower() in ['купить', 'пополнить', 'приобрести',
                            'скупить', 'депозит', 'деп']:
        if len(arg) < 2:
            return await message.reply('❌ Используйте: <code>Грн купить {кол-во}</code>',
                                       reply_markup=my_uah_kb)
        try:
            xa = sql.execute(f'SELECT bank FROM users WHERE id = {message.from_user.id}', False, True)[0][0]
            summ = get_cash(arg[1]) if arg[1].lower() not in ['всё', 'все'] else int(xa / uah_to_usd(1))
            if summ <= 0:
                raise Exception('123')
        except:
            return await message.reply('🚫 Неверный ввод!')
        if (summ + uah.balance) > uah.spaciousness:
            return await message.reply('🚫 Вы превысили лимит вашего сейфа!')
        user_summ = uah_to_usd(summ)

        if user_summ > xa:
            return await message.reply(f'❌ Недостаточно денег в банке! Нужно: {to_str(user_summ)}',
                                       reply_markup=show_balance_kb)

        sql.executescript(f'UPDATE uah SET balance = balance + {summ} WHERE owner = {message.from_user.id};\n'
                          f'UPDATE users SET bank = bank - {user_summ} WHERE id = {message.from_user.id};',
                          True, False)

        await message.reply(f'✅ Вы успешно приобрели {summ} грн за {to_str(user_summ)}',
                            reply_markup=my_uah_kb)

        now = uah_price() + int(summ * random.choice([0.01, 0.05, 0.04, 0.03, 0]))

        await set_uah_price(now)

        return

    elif arg[0].lower() in ['продать', 'снять', 'обменять']:
        try:
            if arg[1].isdigit():
                summ = get_cash(arg[1])
            else:
                raise Exception('123')
        except:
            summ = uah.balance
        if summ <= 0:
            return await message.reply('😴 Кол-во ГРИВЕН меньше или равно нулю!')
        elif summ > uah.balance:
            return await message.reply('😴 Кол-во ГРИВЕН больше чем баланс сейфа!')

        now = uah_price() - int(summ * 0.05)

        await set_uah_price(now)

        user_summ = uah_to_usd(summ)

        sql.executescript(f'UPDATE uah SET balance = balance - {summ} WHERE owner = {message.from_user.id};\n'
                          f'UPDATE users SET bank = bank + {user_summ} WHERE id = {message.from_user.id};',
                          True, False)

        await message.reply(f'✅ Вы успешно сняли {to_str(user_summ)} с сейфа!',
                            reply_markup=my_uah_kb)

        return
    elif arg[0].lower() in ['улучш', 'улучшить', 'boost',
                            'буст', 'повысить']:
        xa = sql.execute(f'SELECT bank FROM users WHERE id = {message.from_user.id}', False, True)[0][0]
        price = 100000 * uah.level
        if xa < price:
            return await message.reply(f'🚫 Недостаточно денег в банке для буста, нужно: {to_str(price)}',
                                       reply_markup=my_uah_kb)

        sql.executescript(f'UPDATE users SET bank = bank - {price} WHERE id = {message.from_user.id};\n'
                          f'UPDATE uah SET level = level + 1 WHERE owner = {message.from_user.id};')
        return await message.reply(f'🥫 Вы улучшили свой сейф ГРН и теперь он вмещает: {to_str((uah.level + 1) * 1000)}',
                                   reply_markup=my_uah_kb)
