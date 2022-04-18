from aiogram.types import Message

from utils.main.users import User


async def ban_user_handler(message: Message):
    arg = message.text.split()
    if arg[0].lower() == '/ban':
        arg = arg[1:]
        if message.reply_to_message:
            admin = User(user=message.from_user)
            reason = ' '.join(arg)
            await User(user=message.reply_to_message.from_user).banf(reason, admin, message.bot)
        elif len(arg) >= 1:
            admin = User(user=message.from_user)
            reason = ' '.join(arg[1:])
            await User(username=arg[0].lower().replace('@', '')).banf(reason, admin, message.bot)
        else:
            return await message.reply('⛔ Неверный формат команды')
        return await message.reply('🟢 Пользователь забанен')
    else:
        arg = arg[1:]
        if message.reply_to_message:
            User(user=message.reply_to_message.from_user).edit('ban', False)
        elif len(arg) == 1:
            User(username=arg[0].lower().replace('@', '')).edit('ban', False)
        else:
            return await message.reply('⛔ Неверный формат команды')
        return await message.reply('🔓 Пользователь разбанен')
