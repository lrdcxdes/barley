from aiogram.types import Message

from config import bot_name
from keyboard.games import play_bowling_kb
from keyboard.generate import show_balance_kb
from utils.main.cash import get_cash, to_str
from utils.main.users import User


async def bowling_handler(message: Message):
    arg = message.text.split()[1:] if not bot_name.lower() in message.text.split()[0].lower() else message.text.split()[2:]
    if len(arg) < 1:
        return await message.reply('❌ Ошибка. Используйте: <code>Боулинг {<i>ставка</i>}</code>')

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

    bow = await message.reply_dice('🎳')
    bow = bow.dice.value

    if bow in [1, 2, 3, 4]:
        user.edit('balance', user.balance - summ)
        return await message.reply(f'👎🏿 Вы проебали {to_str(summ)}',
                                   reply_markup=play_bowling_kb)
    elif bow == 5:
        price = int(summ * float(f'0.{bow}'))
        user.edit('balance', user.balance + price)
        return await message.reply(f'🎳 Вы выиграли и увеличили ставку в (x0.{bow}) ставка после выигрыша: '
                                   f'{to_str(summ + price)}',
                                   reply_markup=play_bowling_kb)
    else:
        price = summ
        user.edit('balance', user.balance + price)
        return await message.reply(f'🎳 Вы выиграли и увеличили ставку в (x2) ставка после выигрыша: '
                                   f'{to_str(summ + price)}',
                                   reply_markup=play_bowling_kb)
