from aiogram.dispatcher.filters import BoundFilter

import config
from utils.main.cash import to_str
from utils.main.users import User


class IsRef(BoundFilter):
    async def check(self, message) -> bool:
        if message.chat.id == message.from_user.id and str(message.get_args()).isdigit():
            try:
                user = User(user=message.from_user, check_ref=True)
            except:
                user = None
            if user is None or user.ref is None:
                if user is None:
                    user = User(user=message.from_user)
                ref_id = int(message.get_args())
                try:
                    ref = User(id=ref_id)
                except:
                    return False
                ref.edit('balance', ref.balance + config.zarefa)
                ref.edit('refs', ref.refs + 1)
                user.edit('ref', ref.id)
                try:
                    await message.bot.send_message(chat_id=ref.id,
                                                   text=f'🤴 Вы пригласили пользователя {user.link} и получили +'
                                                        f'{to_str(config.zarefa)}',
                                                   disable_web_page_preview=True)
                except:
                    return False
