from datetime import timedelta

from aiogram.types import Message, CallbackQuery, ChatMemberAdministrator, ChatMemberOwner, ChatPermissions

from keyboard.main import unmute_kb, unban_kb
from utils.main.donates import to_str
from utils.main.users import User


mute_perms = ChatPermissions(
    can_send_messages=False,
    can_send_media_messages=False,
    can_send_polls=False,
    can_send_other_messages=False,
    can_add_web_page_previews=False,
    can_change_info=False,
    can_invite_users=False,
    can_pin_messages=False
)


async def get_datetime(text: str):
    days, hours, minutes = timedelta(microseconds=1), timedelta(microseconds=1), timedelta(microseconds=1)
    if 'д' in text or 'd' in text:
        if 'д' in text:
            xd = text.split('д')[0]
        else:
            xd = text.split('d')[0]
        if len(xd.split()) == 1:
            xd = xd.split()[0]
        else:
            xd = xd.split()[1]
        days = timedelta(days=int(xd))
    if 'м' in text or 'm' in text:
        if 'м' in text:
            xd = text.split('м')[0]
        else:
            xd = text.split('m')[0]
        if len(xd.split()) == 1:
            xd = xd.split()[0]
        else:
            xd = xd.split()[1]
        minutes = timedelta(minutes=int(xd))
    if 'ч' in text or 'h' in text:
        if 'h' in text:
            xd = text.split('h')[0]
        else:
            xd = text.split('ч')[0]
        if len(xd.split()) == 1:
            xd = xd.split()[0]
        else:
            xd = xd.split()[1]
        hours = timedelta(hours=int(xd))

    result = days + hours + minutes
    return result if result.total_seconds() > 30 else None


async def mute_handler(message: Message):
    bot = await message.chat.get_member(user_id=message.bot.id)
    text = ''
    if not isinstance(bot, (ChatMemberOwner, ChatMemberAdministrator)):
        return await message.reply('🍁 У бота нет админки в чате :(')
    elif not bot.can_delete_messages:
        text += '[+] <code>🗑️ Удаление сообщений</code>\n'
    elif not bot.can_restrict_members:
        text += '[+] <code>👤 Блокировка пользователей</code>\n'
    if text:
        return await message.reply(f'🍁 Боту нужны такие разрешения:\n\n{text}\n\n📞 Администраторы должны выдать их '
                                   f'боту чтобы был доступ к командам модерирования!')

    member = await message.chat.get_member(user_id=message.from_user.id)
    if not isinstance(member, (ChatMemberOwner, ChatMemberAdministrator)):
        return await message.reply('🍁 У вас нет админки в этом чате!')

    arg = message.text.split()[1:]
    if len(arg) == 0:
        return await message.reply('🍁 Используйте: <code>Мут {число} *{ссылка}</code>')

    data = await get_datetime(' '.join(arg[:-1]))
    if data is None:
        data = timedelta(hours=1)

    if message.reply_to_message:
        user = User(user=message.reply_to_message.from_user)
    elif '@' in arg[-1]:
        try:
            user = User(username=arg[-1].replace('@', ''))
        except:
            return await message.reply(f'🍁 Пользователя {arg[-1]} не существует!')
    else:
        return await message.reply('🍁 Вы не указали кому дать мут!')

    try:
        await message.chat.restrict(user_id=user.id,
                                    permissions=mute_perms,
                                    until_date=data)
        return await message.reply(text=f'🍁 Пользователь {user.link} был замучен до <code>{to_str(data)}</code>',
                                   reply_markup=unmute_kb(user.id))
    except Exception as ex:
        return await message.reply(f'🍁 Не удалось замутить {user.link}\n'
                                   f'Ошибка: <code>{ex}</code>',
                                   disable_web_page_preview=True)


async def unmute_handler(message: Message):
    call = message
    if not isinstance(message, Message):
        message = message.message
    bot = await message.chat.get_member(user_id=message.bot.id)
    text = ''
    if not isinstance(bot, (ChatMemberOwner, ChatMemberAdministrator)):
        return await message.reply('🍁 У бота нет админки в чате :(')
    elif not bot.can_delete_messages:
        text += '[+] <code>🗑️ Удаление сообщений</code>\n'
    elif not bot.can_restrict_members:
        text += '[+] <code>👤 Блокировка пользователей</code>\n'
    if text:
        return await message.reply(f'🍁 Боту нужны такие разрешения:\n\n{text}\n\n📞 Администраторы должны выдать их '
                                   f'боту чтобы был доступ к командам модерирования!')

    member = await message.chat.get_member(user_id=call.from_user.id)
    if not isinstance(member, (ChatMemberOwner, ChatMemberAdministrator)):
        return await message.reply('🍁 У вас нет админки в этом чате!')

    if isinstance(call, Message):
        arg = message.text.split()[1:]
        if len(arg) == 0 and not message.reply_to_message:
            return await message.reply('🍁 Используйте: <code>Размут *{ссылка}</code>')

    if isinstance(call, Message):
        if message.reply_to_message:
            user = User(user=message.reply_to_message.from_user)
        else:
            try:
                if '@' in arg[-1]:
                    try:
                        user = User(username=arg[-1].replace('@', ''))
                    except:
                        return await message.reply(f'🍁 Пользователя {arg[-1]} не существует!')
            except:
                return await message.reply('🍁 Вы не указали кого размутить!')
    else:
        user = User(id=int(call.data.split('_')[1]))

    try:
        await message.chat.restrict(user_id=user.id,
                                    permissions=message.chat.permissions,
                                    until_date=0)
        return await message.reply(text=f'🍁 Пользователь {user.link} был размучен!')
    except Exception as ex:
        return await message.reply(f'🍁 Не удалось размутить {user.link}\n'
                                   f'Ошибка: <code>{ex}</code>',
                                   disable_web_page_preview=True)


async def ban_handler(message: Message):
    bot = await message.chat.get_member(user_id=message.bot.id)
    text = ''
    if not isinstance(bot, (ChatMemberOwner, ChatMemberAdministrator)):
        return await message.reply('🍁 У бота нет админки в чате :(')
    elif not bot.can_delete_messages:
        text += '[+] <code>🗑️ Удаление сообщений</code>\n'
    elif not bot.can_restrict_members:
        text += '[+] <code>👤 Блокировка пользователей</code>\n'
    if text:
        return await message.reply(f'🍁 Боту нужны такие разрешения:\n\n{text}\n\n📞 Администраторы должны выдать их '
                                   f'боту чтобы был доступ к командам модерирования!')

    member = await message.chat.get_member(user_id=message.from_user.id)
    if not isinstance(member, (ChatMemberOwner, ChatMemberAdministrator)):
        return await message.reply('🍁 У вас нет админки в этом чате!')

    arg = message.text.split()[1:]
    if len(arg) == 0:
        return await message.reply('🍁 Используйте: <code>Бан {число} *{ссылка}</code>')

    data = await get_datetime(' '.join(arg[:-1]))
    if data is None:
        data = timedelta(seconds=30)

    if message.reply_to_message:
        user = User(user=message.reply_to_message.from_user)
    elif '@' in arg[-1]:
        try:
            user = User(username=arg[-1].replace('@', ''))
        except:
            return await message.reply(f'🍁 Пользователя {arg[-1]} не существует!')
    else:
        return await message.reply('🍁 Вы не указали кого забанить!')

    try:
        await message.chat.unban(user_id=user.id,
                                 only_if_banned=False)
        xd = f'до <code>{to_str(data)}</code>' if data.total_seconds() > 30 else 'навсегда'
        return await message.reply(text=f'🍁 Пользователь {user.link} был забанен {xd}',
                                   reply_markup=unban_kb(user.id))
    except Exception as ex:
        return await message.reply(f'🍁 Не удалось забанить {user.link}\n'
                                   f'Ошибка: <code>{ex}</code>',
                                   disable_web_page_preview=True)


async def unban_handler(message: Message):
    call = message
    if not isinstance(message, Message):
        message = message.message

    bot = await message.chat.get_member(user_id=message.bot.id)
    text = ''
    if not isinstance(bot, (ChatMemberOwner, ChatMemberAdministrator)):
        return await message.reply('🍁 У бота нет админки в чате :(')
    elif not bot.can_delete_messages:
        text += '[+] <code>🗑️ Удаление сообщений</code>\n'
    elif not bot.can_restrict_members:
        text += '[+] <code>👤 Блокировка пользователей</code>\n'
    if text:
        return await message.reply(f'🍁 Боту нужны такие разрешения:\n\n{text}\n\n📞 Администраторы должны выдать их '
                                   f'боту чтобы был доступ к командам модерирования!')

    member = await message.chat.get_member(user_id=call.from_user.id)
    if not isinstance(member, (ChatMemberOwner, ChatMemberAdministrator)):
        return await message.reply('🍁 У вас нет админки в этом чате!')

    arg = message.text.split()[1:]

    if isinstance(call, Message):
        if message.reply_to_message:
            user = User(user=message.reply_to_message.from_user)
        else:
            try:
                if '@' in arg[-1]:
                    try:
                        user = User(username=arg[-1].replace('@', ''))
                    except:
                        return await message.reply(f'🍁 Пользователя {arg[-1]} не существует!')
            except:
                return await message.reply('🍁 Вы не указали кого разбанить!')
    else:
        user = User(id=int(call.data.split('_')[1]))

    try:
        await message.chat.unban(user_id=user.id)
        return await message.reply(text=f'🍁 Пользователь {user.link} был разбанен')
    except Exception as ex:
        return await message.reply(f'🍁 Не удалось разбанить {user.link}\n'
                                   f'Ошибка: <code>{ex}</code>',
                                   disable_web_page_preview=True)
