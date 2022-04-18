from aiogram.types import Message

from config import bot_name
from utils.main.users import User


def get_action(source: str):
    return source.replace('ть', 'л').replace('чь', 'г')


emojis = {
    'выебать': '👉👌',
    'трахнуть': '👉👌',
    'изнасиловать': '👉👌',
    'кончить': '💦',
    'уебать': '👊',
    'ударить': '👊',
    'вьебать': '👊',
    'обнять': '🤗',
    'поцеловать': '😗',
    'засосать': '😛',
    'сжечь': '🔥',
    'убить': '😵',
    'лайкнуть': '💘',
    'застрелить': '🔫',
    'удушить': '😱',
    'поджать': '💪🏼',
    'отжарить': '🔥',
    'подарить': '🎁',
    'украсть': '👩🏼‍🎤',
    'спасти': '💖',
    'сфотографировать': '📸',
    'пригласить': '📩',
    'выпить_с': '🍸',
    'потрогать': '💦',
    'прижать': '💪',
    'раздеть': '👗',
}


async def rp_commands_handler(message: Message):
    arg = message.text.split() if not bot_name.lower() in message.text.split()[0].lower() else message.text.split()[1:]

    if arg[0].lower() == 'рп':
        text = '📃 Список рп-команд:\n\n'
        for item, emoji in emojis.items():
            text += f'[{emoji}] {item.capitalize()}\n'
        return await message.reply(text)

    emoji = emojis[arg[0].lower()]
    action = get_action(arg[0].lower())

    index = 1

    if message.reply_to_message:
        user2 = User(user=message.reply_to_message.from_user)
    elif '@' in arg[1]:
        index = 2
        user2 = User(username=arg[1].replace('@', ''))
    else:
        return await message.reply('🥲 Вы не указали пользователя!')

    user = User(user=message.from_user)

    text = f'[{emoji}] {user.link} {action} {user2.link}'
    if len(arg) >= index+1 and user.donate:
        text += f'\nСо словами: <code>{" ".join(arg[index:])}</code>'
    elif len(arg) >= index+1:
        return await message.reply('❌ Доп. слова в действии доступны только от привилегии <b>💎 VIP</b>')
    return await message.answer(text=text, disable_web_page_preview=True)
