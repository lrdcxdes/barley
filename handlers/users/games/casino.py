import random

from aiogram.types import Message

from config import bot_name
from keyboard.games import play_casino_kb
from keyboard.generate import show_balance_kb
from utils.main.cash import to_str, get_cash
from utils.main.prefixes import prefixes
from utils.main.users import User


values = {
    2: [32, 6, 62, 4, 2, 49, 59, 48, 63, 44, 38, 21, 32, 16, 3, 23, 44, 54, 27, 33,
        42, 11, 41, 13, 24, 17],
    3: [43, 11, 22]
}


async def casino_handler(message: Message):
    arg = message.text.split()[1:] if not bot_name.lower() in message.text.split()[0].lower() else message.text.split()[2:]
    if len(arg) == 0:
        return await message.reply('❌ Ошибка. Используйте: <code>Казино {<i>ставка</i>}</code>')

    user = User(user=message.from_user)

    try:
        summ = ssumm = get_cash(arg[0] if arg[0].lower() not in ['всё', 'все'] else str(user.balance))
    except:
        summ = ssumm = 0
    if summ <= 0:
        return await message.reply('❌ Ошибка. Ставка меньше или равна нулю')

    if user.balance < summ:
        return await message.reply('❌ Ошибка. Недостаточно денег на руках для ставки! 💸',
                                   reply_markup=show_balance_kb)

    casino = (await message.reply_dice(emoji='🎰')).dice

    if user.prefix and casino.value not in values[2] and casino.value not in values[3] and casino.value != 64:
        xd = {i["emoji"]: i for i in prefixes.values()}[user.prefix]["price"]
        casino.value -= random.randint(-len(str(xd)), len(str(xd)))

    if casino.value in values[2]:
        summ = int(summ * 1.35)
        user.edit('balance', user.balance + summ - ssumm)
        return await message.reply(f'🎰 Вы умножили свою ставку на (x1.35) и получили +{to_str(summ)} на баланс!',
                                   reply_markup=play_casino_kb)
    elif casino.value in values[3]:
        summ = int(summ * 2)
        user.edit('balance', user.balance + summ - ssumm)
        return await message.reply(f'🎰 Вы умножили свою ставку на (x2) и получили +{to_str(summ)} на баланс!',
                                   reply_markup=play_casino_kb)
    elif casino.value == 64:
        summ = int(summ * 4)
        user.edit('balance', user.balance + summ - ssumm)
        return await message.reply(f'🎰 Вы умножили свою ставку на (x4) и получили +{to_str(summ)} на баланс!',
                                   reply_markup=play_casino_kb)
    else:
        user.edit('balance', user.balance - summ)
        return await message.reply(f'😖 Ваша ставка была умножена на (x0) и вы потеряли {to_str(summ)}!',
                                   reply_markup=play_casino_kb)
