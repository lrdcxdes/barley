from aiogram.types import Message

from config import bot_name
from keyboard.main import check_ls_kb
from loader import bot
from utils.main.users import User


async def refferal_handler(message: Message):
    user = User(user=message.from_user)
    if user.id == message.chat.id:
        return await message.reply(f'✨ Реферальная система бота @{bot_name}\n'
                                   f'🔗 Ваша персональная ссылка: https://t.me/{bot_name}?start={user.id}\n'
                                   f'👥 Кол-во приглашённых людей: <b>{user.refs}</b>', disable_web_page_preview=True)
    else:
        try:
            await bot.send_message(text=f'✨ Реферальная система бота @{bot_name}\n'
                                   f'🔗 Ваша персональная ссылка: https://t.me/{bot_name}?start={user.id}\n'
                                   f'👥 Кол-во приглашённых людей: <b>{user.refs}</b>', disable_web_page_preview=True, chat_id=user.id)
            return await message.reply('👥 Реф-Меню было отправлено в личку с ботом!',
                                       reply_markup=check_ls_kb)
        except:
            return await message.reply('🙃 Вы никогда не писали боту в лс, я не могу отправить вам реф-меню',
                                       reply_markup=check_ls_kb)
