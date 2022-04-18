from aiogram.types import Message

from config import bot_name
from utils.bosses import get_global_boss
from utils.main.users import User


async def bosses_handler(message: Message):
    arg = message.text.split()[1:] if not bot_name.lower() in message.text.split()[0].lower() else message.text.split()[2:]
    boss = await get_global_boss()

    if len(arg) == 0 or arg[0] not in ['бить', 'ударить', 'уебать',
                                       'убить', 'играть', 'побить']:
        msg = await message.reply_photo(caption=boss.text,
                                         photo=boss.photo)
        boss.photo = msg.photo[0].file_id

    else:
        if boss.users.get(message.from_user.id) is not None and boss.users[message.from_user.id] >= 5:
            return await message.reply('Вы уже использовали все попытки на этого босса!\n'
                                       'Дождитесь следующего!')

        result = await boss.push(message.from_user.id)
        user = User(user=message.from_user)
        if type(result) == int:
            user.edit('balance', user.balance + result.result)
        else:
            user.items = list(user.items)
            user.set_item(item_id=int(result.result), x=1)
        return await message.reply(result.text)
