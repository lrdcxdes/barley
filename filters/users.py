from aiogram.dispatcher.filters import BoundFilter
from aiogram.types import Message

from utils.main.users import User


class IsPremium(BoundFilter):
    async def check(self, message: Message) -> bool:
        user = User(user=message.from_user)
        donate = user.donate
        return donate and donate.id > 1


class IsAdmin(BoundFilter):
    async def check(self, message: Message) -> bool:
        user = User(user=message.from_user)
        donate = user.donate
        return donate and donate.id > 2


class IsBan(BoundFilter):
    async def check(self, message: Message) -> bool:
        user = User(user=message.from_user)
        return user.ban
