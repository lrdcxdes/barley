from aiogram.dispatcher.filters import BoundFilter
from config import owner_id


class IsOwner(BoundFilter):
    async def check(self, message):
        return message.from_user.id == owner_id


class IsBot(BoundFilter):
    async def check(self, message):
        return message.new_chat_members[-1].id == message.bot.id
