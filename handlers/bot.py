from aiogram.types import Message

from utils.main.chats import Chat


async def bot_added_to_chat(message: Message):
    Chat(chat=message.chat)
    return await message.answer('<a href="https://t.me/barleygamebot">✨</a> Спасибо что добавили меня в чат!\n'
                                '😇 Помощь: /help (все доступные команды)\n' 
                                '🅰️ Админ: <a href="https://t.me/lord_code">@admin</a>\n' 
                                '💒 Игровой чат: @barleychat\n'
                                '🗞️ Новости и промокоды: @barleygame\n'
                                )
