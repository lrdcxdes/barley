import random

from aiogram.types import Message

from config import bot_name
from keyboard.games import play_cnb_kb
from keyboard.generate import show_balance_kb
from utils.main.cash import get_cash, to_str
from utils.main.users import User


async def cnb_handler(message: Message):
    arg = message.text.split()[1:] if not bot_name.lower() in message.text.split()[0].lower() else message.text.split()[2:]
    if len(arg) < 2:
        return await message.reply('❌ Ошибка. Используйте: <code>Кнб {<i>ставка</i>} {камень/ножницы/бумага}</code> ('
                                   'к/н/б)')

    user = User(user=message.from_user)

    try:
        summ = get_cash(arg[0] if arg[0].lower() not in ['всё', 'все'] else str(user.balance))
    except:
        summ = 0
    if summ <= 0:
        return await message.reply('❌ Ошибка. Ставка меньше или равна нулю')

    if user.balance < summ:
        return await message.reply('❌ Ошибка. Недостаточно денег на руках для ставки! 💸',
                                   reply_markup=show_balance_kb)

    lower = arg[1].lower()

    user_c = 'Камень 🪨' if lower.startswith('к') else 'Ножницы ✂️' if lower.startswith('н') else 'Бумага 🧻'

    choice = random.choice(['Камень 🪨', 'Ножницы ✂️', 'Бумага 🧻'])

    text = f'Вы загадали <b>{user_c}</b> а я выбрал <b>{choice}</b>'

    if (user_c == 'Камень 🪨' and choice == 'Ножницы ✂️') or (user_c == 'Ножницы ✂️' and choice == 'Бумага 🧻') or (
            user_c == 'Бумага 🧻' and choice == 'Камень 🪨'):
        summ *= 2
        user.edit('balance', user.balance + summ // 2)
        text = text + f'\n💲 Вы удвоили свою ставку (x2) и получили +{to_str(summ)}'
    else:
        user.edit('balance', user.balance - summ)
        text = text + f'\n💲 Вы проебали {to_str(summ)}'
    return await message.reply(text=text, reply_markup=play_cnb_kb)
