from aiogram.types import Message

from config import bot_name
from keyboard.games import play_dice_kb
from keyboard.generate import show_balance_kb
from utils.logs import writelog
from utils.main.cash import to_str, get_cash
from utils.main.users import User


async def dice_handler(message: Message):
    arg = message.text.split()[1:] if not bot_name.lower() in message.text.split()[0].lower() else message.text.split()[2:]
    if len(arg) < 2:
        return await message.reply('❌ Ошибка. Используйте: <code>Кубик {<i>ставка</i>} {<i>число 1-6</i>}</code>')
    elif not arg[0].isdigit() or not arg[1].isdigit() or int(arg[0]) <= 0:
        return await message.reply('❌ Ошибка. Используйте: <code>Кубик {<i>ставка</i>} {<i>число 1-6</i>}</code>')

    user = User(user=message.from_user)

    summ = get_cash(arg[0] if arg[0].lower() not in ['всё', 'все'] else str(user.balance))
    index = int(arg[1])

    if user.balance < summ:
        return await message.reply('❌ Ошибка. Недостаточно денег на руках для ставки! 💸',
                                   reply_markup=show_balance_kb)
    elif index < 1 or index > 6:
        return await message.reply('❌ Ошибка. Число должно быть от 1 до 6!')

    dice = (await message.reply_dice()).dice
    if dice.value != index:
        user.edit('balance', user.balance - summ)
        await message.reply(f'😖 Вы не угадали число, вам выпало {dice.value} а вы загадали {index}. К сожалению '
                            f'вы '
                            f'проиграли '
                            'деньги!',
                            reply_markup=play_dice_kb)
        await writelog(message.from_user.id, f'Кубик и проигрыш')
        return
    x = int(summ * 1.5)
    user.edit('balance', user.balance + x - summ)
    await message.reply(f'🏅 Вы угадали число! На ваш баланс зачислено +{to_str(x)}',
                        reply_markup=play_dice_kb)
    await writelog(message.from_user.id, f'Кубик и победа')
    return
