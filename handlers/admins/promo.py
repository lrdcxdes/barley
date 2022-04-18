from aiogram.types import Message

from utils.main.cash import to_str, get_cash
from utils.promo.promo import Promocode


async def promo_handler(message: Message):
    args = message.text.split()[1:]
    try:
        name, summ, activations = tuple(args)
        xd = 1
    except:
        name, summ, activations, xd = tuple(args)
    Promocode.create(name, int(activations), get_cash(summ), int(xd))

    return await message.reply(f'🪄 Промокод <code>{name}</code> на сумму {to_str(int(summ))} и кол-во активаций'
                               f' <b>{activations}</b> успешно создан')
