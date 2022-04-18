from aiogram.types import Message

from config import bot_name
from keyboard.generate import show_balance_kb
from keyboard.main import prefix_buy_kb
from utils.main.cash import to_str
from utils.main.prefixes import prefixes
from utils.main.users import User


async def prefix_handler(message: Message):
    arg = message.text.split()[1:] if not bot_name.lower() in message.text.split()[0].lower() else message.text.split()[2:]

    if len(arg) == 0:
        text = f'📃 Все доступные префиксы:\n' \
               f'<i>Номер. Название - цена</i>\n\n'
        for index, prefix in prefixes.items():
            text += f'<code>{index}</code>. <b>{prefix["name"]} {prefix["emoji"]}</b> - {to_str(prefix["price"])}\n'

        text += '\n\nВведите: <code>Префикс купить {номер}</code>'

        return await message.reply(text, reply_markup=prefix_buy_kb)

    elif arg[0].lower() in ['купить', 'приобрести', 'buy']:
        if len(arg) < 2:
            return await message.reply('❌ Вы не ввели номер префикса!')
        elif int(arg[1]) < 1 or int(arg[1]) > len(prefixes):
            return await message.reply('❌ Вы ввели неверный номер префикса!')

        user = User(user=message.from_user)

        prefix = prefixes[int(arg[1])]

        if user.balance < prefix['price']:
            return await message.reply(f'💲 Недостаточно денег на руках для покупки. Нужно: {to_str(prefix["price"])}',
                                       reply_markup=show_balance_kb)
        elif user.donate:
            return await message.reply('❌ Эх... У вас есть донат и вы не можете купить префикс!')

        user.set_prefix(prefix)

        return await message.reply(f'✅ Вы успешно приобрели префикс <b>{prefix["name"]} {prefix["emoji"]}</b>',
                                   reply_markup=show_balance_kb)

    else:
        return await message.reply('❌ Используйте: <code>Префикс купить {номер}</code>')
