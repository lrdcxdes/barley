import random

from aiogram.types import Message

from config import bot_name
from keyboard.games import play_roulette_kb
from keyboard.generate import show_balance_kb
from utils.logs import writelog
from utils.main.cash import to_str, get_cash
from utils.main.users import User


async def roulette_handler(message: Message):
    arg = message.text.split()[1:] if not bot_name.lower() in message.text.split()[0].lower() else message.text.split()[2:]
    if len(arg) < 3 or arg[1].lower() not in ["red", "green", 'black',
                                                                      "красный", "зеленый",
                                                                      'зелёный', 'черный', "чёрный",
                                                                      '⚫', '🔴', '🟢'] or \
            not arg[2].isdigit() or int(arg[2]) <= 0 or int(arg[2]) > 100:
        return await message.reply('❌ Ошибка. Используйте: <code>Рулетка {ставка} {цвет ("red", "green", '
                                   '"black")} {число до 100}</code>')
    color = {
        "красный": "🔴",
        "зелёный": '🟢',
        'зеленый': '🟢',
        'чёрный': '⚫',
        'черный': '⚫',
        'red': '🔴',
        'green': '🟢',
        'black': '⚫'
    }.get(arg[1].lower())
    if color is None:
        return await message.reply('❌ Ошибка. Используйте: <code>Рулетка {ставка} {цвет ("red", "green", '
                                   '"black")} {число до 100}</code>')

    user = User(user=message.from_user)

    try:
        summ = get_cash(arg[0] if arg[0].lower() not in ['всё', 'все'] else str(user.balance))
    except:
        summ = 0
    if summ <= 0:
        return await message.reply('❌ Ошибка. Используйте: <code>Рулетка {ставка} {цвет ("red", "green", '
                                   '"black")} {число до 100}</code>')

    if user.balance < summ:
        return await message.reply('❌ Ошибка. Недостаточно денег на руках для ставки 💸',
                                   reply_markup=show_balance_kb)

    index = int(arg[2])

    game_index, game_color = random.randint(1, 100), random.choices('⚫🟢🔴', weights=(50, 1, 50))[0]
    if game_color != color:
        user.edit('balance', user.balance - summ)
        await message.reply(f'😖 Вы проиграли. Вам выпало {game_index}{game_color}!',
                            reply_markup=play_roulette_kb)
        await writelog(message.from_user.id, f'Рулетка и проигрыш')
        return
    else:
        result = abs(index - game_index)
        win = int((summ * 2) * float(f'0.{result}'))
        user.edit('balance', user.balance + win - summ)
        await message.reply(f'Вам выпало {game_index}{game_color} и вы получили +{to_str(win)}',
                            reply_markup=play_roulette_kb)
        await writelog(message.from_user.id, f'Рулетка и выигрыш')
        return
