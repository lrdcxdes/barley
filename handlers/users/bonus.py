from datetime import datetime, timedelta

from aiogram.types import Message

from utils.logs import writelog
from utils.main.cash import to_str
from utils.main.donates import to_str as to_strs
from utils.main.users import User

day = 60 * 60 * 24


async def bonus_handler(message: Message):
    user = User(user=message.from_user)
    dop = '\n\nДобавь к своему телеграм имени или фамилии "@barleygamebot" и <b>получай +25% к бонусу</b>'
    if (datetime.now() - user.bonus).total_seconds() < day and datetime.now().day <= user.bonus.day:
        return await message.reply('❌ Вы уже забирали ежедневный бонус\n'
                                   f'⏳ Следующий через: <code>'
                                   f'{to_strs((user.bonus + timedelta(days=1)) - datetime.now())}</code>' + dop)
    else:
        xax = message.from_user.full_name
        if message.chat.id == message.from_user.id and message.chat.description:
        	xax += f' {message.chat.description}'
        bonus = user.get_bonus(xax)
        await message.reply(f'✅ Вы активировали ежедневный бонус,'
                            f' на ваш баланс зачислено +{to_str(bonus)}')
        await writelog(message.from_user.id, f'Активация ежедневного бонуса!' + dop)
        return
