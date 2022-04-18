from aiogram.types import Message
import random

from config import bot_name
from keyboard.jobs import bottle_kb
from utils.items.items import items
from utils.logs import writelog
from utils.main.cash import to_str
from utils.main.users import User
import time


async def bottles_handler(message: Message):
    if 'бутылки' in message.text.lower() or 'бутылка' in message.text.lower():
        arg = message.text.split()[1:] if not bot_name.lower() in message.text.split()[0].lower() else message.text.split()[2:]
    else:
        arg = message.text.split()[1:] if bot_name.lower() in message.text.split()[0].lower() else message.text.split()

    user = User(user=message.from_user)

    xd = [27]
    if user.xp >= 100:
        xd.append(28)
    else:
        xd.append(27)
    if user.xp >= 300:
        xd.append(29)
    else:
        xd.append(27)
    if user.xp >= 500:
        xd.append(30)
    else:
        xd.append(27)
    xd.append(random.choice([1, 5, 6, 7, 8, 10]))

    if len(arg) == 0:
        text = ''
        for index, i in enumerate(list(range(27, 30))):
            item = items[i]
            a = f'<code>{index}</code>. <b>{item["name"]} {item["emoji"]}</b> - {to_str(item["sell_price"])} (♟️ ' \
                f'{item["xp"]})\n'
            if i in xd:
                text += a
            else:
                text += '<tg-spoiler>' + a + '</tg-spoiler>'
        return await message.reply(f'👨🏿‍🦲 Доступные вам бутылки:\n' + text + '\n\n'
                                   + f'⚡ Энергия: {user.energy}, ♟️ Опыт: {user.xp}',
                                   reply_markup=bottle_kb)

    elif user.energy <= 0:
        return await message.reply('⚡ У вас недостаточно энергии.')

    elif arg[0] == 'искать' or arg[0] == 'собирать':
        try:
            count = int(arg[1])
            if count < 1:
                raise Exception('123')
        except:
            count = 1
        if count > user.energy:
            return await message.reply('У вас нет столько энергии!')
        laste = user.energy
        user.editmany(energy=laste - count,
                      xp=user.xp + count,
                      energy_time=time.time())
        w = [1.0 for _ in range(len(xd) - 1)]
        w.append(0.1)
        item_id = random.choices(xd, k=count, weights=w)
        item_counts = []
        completed = {}
        for index, i in enumerate(item_id):
            if i in completed:
                item_counts[completed[i]] += random.randint(1, 30) if i not in [1, 5, 6, 7, 8,
                                                                                10] else random.randint(1, 10)
            else:
                completed[i] = len(item_counts)
                item_counts.append(random.randint(1, 30) if i not in [1, 5, 6, 7, 8, 10] else random.randint(1, 10))

        user.items = list(user.items)
        item_id = list(completed.keys())
        user.set_item_many(item_ids=item_id, counts=item_counts)

        text = ''
        for i, index in completed.items():
            x = i
            i = items[i]
            count = item_counts[completed[x]]
            text += f'<code>+{count}</code> <b>{i["name"]}' \
                    f' {i["emoji"]}</b>\n'

        await message.reply(f'👨🏿‍🦲 Вы добыли {text}\n'
                            f'♟️ XP: <code>{user.xp}</code>\n'
                            f'⚡ Энергия: <code>{user.energy}</code>')
        await writelog(message.from_user.id, f'Добыча {text}\n с шахты')
        return
