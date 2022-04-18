from aiogram.types import Message

from config import bot_name
from keyboard.main import top_kb
from utils.main.cash import to_str
from utils.main.db import sql
from utils.main.users import User

numbers_emoji = ['0️⃣', '1️⃣', '2️⃣', '3️⃣', '4️⃣', '5️⃣', '6️⃣', '7️⃣', '8️⃣', '9️⃣']


async def top_handler(message: Message):
    text = '🔝 Пользователей по ({}):\n' \
           '<i>🎄 Всего пользователей: {}</i>\n\n'
    arg = ' '.join(message.text.split()[1:] if not bot_name.lower() in message.text.split()[0].lower() else message.text.split()[2:])
    if len(arg) == 0 or 'общ' in arg.lower() or 'все' in arg.lower() or 'всё' in arg.lower():
        top_users = sql.execute('SELECT id, first_name, name, username, deposit+bank+balance, prefix FROM users ORDER BY '
                                'deposit+bank+balance DESC;',
                                False,
                                True)
    elif True in [i in arg.lower() for i in ['рук', 'деньг', 'кэш', 'бабк']]:
        top_users = sql.execute('SELECT id, first_name, name, username, balance, prefix FROM users ORDER BY balance DESC;',
                                False,
                                True)
    elif 'бан' in arg.lower():
        top_users = sql.execute('SELECT id, first_name, name, username, bank, prefix FROM users ORDER BY bank DESC;',
                                False,
                                True)
    elif 'деп' in arg.lower():
        top_users = sql.execute('SELECT id, first_name, name, username, deposit, prefix FROM users ORDER BY deposit DESC;',
                                False,
                                True)
    elif 'уровень' in arg.lower():
        top_users = sql.execute('SELECT id, first_name, name, username, level, prefix FROM users ORDER BY level DESC;',
                                False,
                                True)
    elif 'реф' in arg.lower():
        top_users = sql.execute('SELECT id, first_name, name, username, refs, prefix FROM users ORDER BY refs DESC;',
                                False,
                                True)
    elif 'бра' in arg.lower() or 'сем' in arg.lower():
        top_marries = sql.execute('SELECT user1, user2, name, level FROM marries ORDER BY level DESC;',
                                  False,
                                  True)
        text = '🔝 Семей по уровню:\n' \
               f'<i>🎄 Всего семей: {len(top_marries)}</i>\n\n'

        for index, user in enumerate(top_marries[:10], start=1):
            emoji = ''.join(numbers_emoji[int(i)] for i in str(index))
            user1, user2, name, level = user
            user1, user2 = User(id=user1), User(id=user2)
            link = f'{user1.link} & {user2.link}' if name is None else name
            text += f'{emoji}. {link} - {level}\n'

        return await message.reply(text=text, disable_web_page_preview=True,
                                   reply_markup=top_kb)

    else:
        return await message.reply('❌ Неверный аргумент. Используйте: <code>Топ ['
                                   'деньги|банк|деп|общий|уровень|семьи]</code>')

    try:
        text = text.format(
            arg.lower().split()[0] if arg.lower().split()[0] != 'по' else arg.lower().split()[1],
            len(top_users))
    except:
        text = text.format('балансу', len(top_users))

    for index, user in enumerate(top_users[:10], start=1):
        emoji = ''.join(numbers_emoji[int(i)] for i in str(index))
        user_id, first_name, name, username, balance, prefix = user
        link = f'<a href="https://t.me/{username}">{name if name else first_name}</a>' \
            if username else f'<a href="tg://user?id={user_id}">{name if name else first_name}</a>'
        text += f'{emoji}. {prefix + " " if prefix and name else ""}{link} - ' \
                f'{to_str(balance) if not (True in [i in arg.lower() for i in ["уровень", "реф", "лвл"]]) else balance}\n'
    text += '➖➖➖➖➖➖➖➖➖➖➖➖➖\n'
    for index, user_s in enumerate(top_users, start=1):
        if user_s[0] == message.from_user.id:
            index = index
            break
    emoji = ''.join(numbers_emoji[int(i)] for i in str(index + 1))
    user_id, first_name, name, username, balance, prefix = user_s
    link = f'<a href="https://t.me/{username}">{name if name else first_name}</a>' \
        if username else f'<a href="tg://user?id={user_id}">{name if name else first_name}</a>'
    text += f'{emoji}. {prefix + " " if prefix and name else ""}{link} - ' \
            f'{to_str(balance) if not (True in [i in arg.lower() for i in ["уровень", "реф", "лвл"]]) else balance}\n'

    return await message.reply(text=text, disable_web_page_preview=True,
                               reply_markup=top_kb)
