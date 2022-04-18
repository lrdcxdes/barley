import time

from aiogram.types import Message

from config import bot_name
from keyboard.generate import show_balance_kb, show_house_kb, house_kb, buy_house_kb
from utils.logs import writelog
from utils.main.cash import to_str, get_cash
from utils.main.houses import House, houses
from utils.main.db import sql


async def house_list_handler(message: Message):
    text = 'Название - цена - доход - налог\n'
    asd = sql.execute(f'SELECT sell_count FROM users WHERE id = {message.from_user.id}', False, True)[0][0]
    if asd is None:
        asd = 0
    xa = asd = float(f'0.{asd}')
    for index, i in houses.items():
        price = i["price"] - int(i["price"] * xa)
        text += f'<code>{index}</code>. {i["name"]} - {to_str(price)} - {to_str(i["doxod"])}' \
                f' - {to_str(i["nalog"])}\n'
    return await message.reply(
                               f'<i>(Ваша скидка: x{asd})</i>\n\n'
                               + text + '\n\nИспользуйте: <code>Дом купить {номер}</code> чтобы купить!',
    reply_markup=buy_house_kb)


async def house_handler(message: Message):
    arg = message.text.split()[1:] if not bot_name.lower() in message.text.split()[0].lower() else message.text.split()[2:]
    try:
        house = House(user_id=message.from_user.id)
    except:
        house = None
        if len(arg) < 1 or arg[0].lower() != 'купить' or not arg[1].isdigit():
            return await house_list_handler(message)
    if len(arg) == 0:
        return await message.reply(text=house.text, reply_markup=house_kb)
    elif arg[0].lower() in ['список', 'лист']:
        return await house_list_handler(message)
    elif arg[0].lower() == 'продать':
        doxod = house.sell()
        sql.execute(f'UPDATE users SET bank = bank + {doxod} WHERE id = {message.from_user.id}', True, False)
        await message.reply(f'✅ Вы продали дом и с учётом налогов, и дохода вы получили: {to_str(doxod)}',
                            reply_markup=show_balance_kb)
        await writelog(message.from_user.id, f'Продажа дома!')
        return
    elif arg[0].lower() == 'купить':
        if house:
            return await message.reply('❗ У вас уже есть дом, можно иметь только 1.',
                                       reply_markup=show_house_kb)
        try:
            i = houses[int(arg[1])]
        except:
            return await message.reply('❌ Ошибка. Неверный номер дома!')

        xa = sql.execute(f'SELECT sell_count, balance FROM users WHERE id = {message.from_user.id}', False, True)[0]
        balance = xa[1]
        xa = xa[0]
        if xa is None:
            xa = 0
        xa = float(f'0.{xa}')
        price = i["price"] - int(i["price"] * xa)

        if balance < price:
            return await message.reply(f'💲 На руках недостаточно денег для покупки, нужно: '
                                       f'{to_str(price)}',
                                       reply_markup=show_balance_kb)
        House.create(user_id=message.from_user.id, house_index=int(arg[1]))

        sql.execute(f'UPDATE users SET balance = balance - {price}, sell_count = 0 WHERE id ='
                    f' {message.from_user.id}', True)
        await message.reply(f'✅ Вы успешно приобрели хату {i["name"]} за {to_str(price)}',
                            reply_markup=show_house_kb)
        await writelog(message.from_user.id, f'Покупка дома')
        return
    elif arg[0].lower() in ['аренда', 'сдать']:
        house.editmany(arenda=not house.arenda, last=time.time() if (not house.arenda) is True else None)
        await message.reply('🅰️ Вы сдали в аренду свой дом!' if house.arenda else
                                   '🅰️ Вы сняли с аренды свой дом!',
                            reply_markup=show_house_kb)
        await writelog(message.from_user.id, f'Сдача в аренду дома')
        return
    elif arg[0].lower() in ['снять', 'доход']:
        xd = house.cash
        if len(arg) > 1:
            try:
                xd = get_cash(arg[1])
            except:
                pass
        if house.cash < xd or house.cash < 0:
            return await message.reply('💲 Недостаточно денег на счету дома!')
        elif xd <= 0:
            return await message.reply('❌ Нельзя так!')
        sql.executescript(f'''UPDATE users SET bank = bank + {xd} WHERE id = {message.from_user.id};
        UPDATE houses SET cash = {house.cash - xd} WHERE id = {house.id};''', True)

        await message.reply(f'✅ Вы успешно сняли {to_str(xd)} с прибыли дома!',
                            reply_markup=show_house_kb)
        await writelog(message.from_user.id, f'Снятие {to_str(xd)} с прибыли дома')
        return
    elif arg[0].lower() in ['оплата', 'оплатить', 'налог', 'налоги']:
        xd = house.nalog
        if len(arg) > 1:
            try:
                xd = get_cash(arg[1])
            except:
                pass
        if house.nalog < 1:
            return await message.reply('💲 Налог на дом и так оплачен!')
        elif house.nalog < xd:
            xd = house.nalog
        elif xd <= 0:
            return await message.reply('❌ Нельзя так!')
        if sql.execute(f'SELECT bank FROM users WHERE id = {message.from_user.id}', False, True)[0][0] < xd:
            await message.reply(f'💲 Недостаточно денег в банке для оплаты налога, нужно: {to_str(xd)}!',
                                reply_markup=show_balance_kb)
            await writelog(message.from_user.id, f'Оплата налога на дом')
            return

        sql.executescript(f'''UPDATE users SET bank = bank - {xd} WHERE id = {message.from_user.id};
                UPDATE houses SET nalog = {house.nalog - xd} WHERE id = {house.id};''', True)

        return await message.reply('✅ Налог на дом успешно оплачен!')
    else:
        return await message.reply('❌ Ошибка. Используйте: <code>Дом [снять|сдать|оплатить] *{сумма}</code>')
