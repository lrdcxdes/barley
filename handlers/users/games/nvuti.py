import random

from aiogram.types import Message

from config import bot_name
from keyboard.games import play_nvuti_kb
from keyboard.generate import show_balance_kb
from utils.logs import writelog
from utils.main.cash import to_str, get_cash
from utils.main.users import User


async def nvuti_handler(message: Message):
    arg = message.text.split()[1:] if not bot_name.lower() in message.text.split()[0].lower() else message.text.split()[2:]
    if len(arg) < 2 or not arg[1] in ['<', '>', '=']:
        return await message.reply('❌ Ошибка. Используйте: `Нвути {ставка} {знак (<,>,=)}`', parse_mode='markdown')

    user = User(user=message.from_user)

    try:
        summ = get_cash(arg[0] if arg[0].lower() not in ['всё', 'все'] else str(user.balance))
    except:
        summ = 0
    if summ <= 0:
        return await message.reply('❌ Ошибка. Используйте: `Нвути {ставка} {знак (<,>,=)}`', parse_mode='markdown')
    znak = arg[1]

    if user.balance < summ:
        return await message.reply('❌ Ошибка. Недостаточно денег на руках для ставки! 💸',
                                   reply_markup=show_balance_kb)

    result = random.randint(1, 100)
    if result < 50 and znak == '<':
        znak_result = '📉'
        win = True
    elif result == 50 and znak == '=':
        znak_result = '📈'
        win = True
    elif result > 50 and znak == '>':
        znak_result = '📈'
        win = True
    else:
        znak_result = '📈' if result >= 50 else '📉'
        win = False

    if not win:
        user.edit('balance', user.balance - summ)
        await message.reply(f'{znak_result} Вы проиграли, число {result} не {znak} 50', parse_mode='markdown',
                            reply_markup=play_nvuti_kb)
        await writelog(message.from_user.id, f'Нвути и проигрыш')
        return

    user.edit('balance', user.balance + (int(summ * 1.5) - summ))
    await message.reply(f'{znak_result} Вы выиграли, число {result} {znak} 50 на ваш баланс зачислено +'
                        f'{to_str(int(summ * 1.5))}'.replace('<code>', '`').replace('</code>',
                                                                                    '`'),
                        parse_mode='markdown',
                        reply_markup=play_nvuti_kb)
    await writelog(message.from_user.id, f'Нвути и победа')
    return
