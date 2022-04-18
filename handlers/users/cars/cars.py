from aiogram.types import Message

from config import bot_name
from keyboard.generate import show_balance_kb, show_inv_kb, show_car_kb, car_kb, buy_car_kb, ride_car_kb
from utils.logs import writelog
from utils.main.cars import cars, Car
from utils.main.cash import to_str, get_cash
from utils.main.db import sql


async def cars_list_handler(message: Message):
    text = 'Название - цена - сток - налог\n'
    asd = sql.execute(f'SELECT sell_count FROM users WHERE id = {message.from_user.id}', False, True)[0][0]
    if asd is None:
        asd = 0
    xa = float(f'0.{asd}')
    for index, i in cars.items():
        price = i["price"] - int(i["price"] * xa)
        text += f'<code>{index}</code>. {i["name"]} - {to_str(price)} - {i["fuel"]}' \
                f' - {to_str(i["nalog"])}\n'
    return await message.reply(
        f'<i>(Ваша скидка: x{asd})</i>\n\n'
        + text + '\n\nИспользуйте: <code>Машина купить {номер}</code> чтобы купить!',
        reply_markup=buy_car_kb)


async def cars_handler(message: Message):
    arg = message.text.split()[1:] if not bot_name.lower() in message.text.split()[0].lower() else message.text.split()[2:]
    try:
        car = Car(user_id=message.from_user.id)
    except:
        car = None
        if len(arg) < 1 or arg[0].lower() != 'купить' or not arg[1].isdigit():
            return await cars_list_handler(message)
    if len(arg) == 0:
        return await message.reply(text=car.text, reply_markup=car_kb)
    elif arg[0].lower() in ['список', 'лист']:
        return await cars_list_handler(message)

    elif arg[0].lower() == 'продать':
        doxod = car.sell()
        sql.execute(f'UPDATE users SET bank = bank + {doxod} WHERE id = {message.from_user.id}')
        await message.reply(f'✅ Вы продали машину и с учётом налогов, и дохода вы получили: {to_str(doxod)}',
                            reply_markup=show_balance_kb)
        await writelog(message.from_user.id, f'Машина продажа')
        return
    elif arg[0].lower() == 'купить':
        if car:
            return await message.reply('❗ У вас уже есть машина, можно иметь только 1.',
                                       reply_markup=show_car_kb)
        try:
            i = cars[int(arg[1])]
        except:
            return await message.reply('❌ Ошибка. Неверный номер машины!')
        xa = sql.execute(f'SELECT sell_count, balance FROM users WHERE id = {message.from_user.id}', False, True)[0]
        balance = xa[1]
        xa = xa[0]
        if xa is None:
            xa = 0
        xa = float(f'0.{xa}')
        price = i["price"] - int(i["price"] * xa)

        if balance < price:
            return await message.reply(
                f'💲 На руках недостаточно денег для покупки, нужно: {to_str(price)}')
        Car.create(user_id=message.from_user.id, car_index=int(arg[1]))
        sql.execute(f'UPDATE users SET balance = balance - {price}, sell_count = 0 WHERE id ='
                    f' {message.from_user.id}', True)
        return await message.reply(f'✅ Вы успешно приобрели машину <b>{i["name"]}</b> за'
                                   f' {to_str(price)}', reply_markup=show_car_kb)
    elif arg[0].lower() in ['снять', 'доход']:
        xd = car.cash
        if len(arg) > 1:
            try:
                xd = get_cash(arg[1])
            except:
                pass
        if car.cash < xd or car.cash < 0:
            return await message.reply('💲 Недостаточно денег на счету машины!', reply_markup=show_car_kb)
        elif xd <= 0:
            return await message.reply('❌ Нельзя так!')
        sql.executescript(f'''UPDATE users SET bank = bank + {xd} WHERE id = {message.from_user.id};
                              UPDATE cars SET cash = cash - {xd} WHERE id = {car.id};''',
                          True)

        await message.reply(f'✅ Вы успешно сняли {to_str(xd)} с прибыли машины!', reply_markup=show_balance_kb)
    elif arg[0].lower() in ['ехать', 'зарабатывать', 'заработать', 'работать',
                            'работа', 'лететь', 'летать']:
        if car.fuel <= 0:
            return await message.reply('🏎️ Машина больше не может ехать! Её состояние: 0%\n'
                                       'Вам нужно <b>Болтик 🔩</b> (x10) чтобы восстановить 1%\n\nВведите <code>'
                                       ' Машина починить</code> чтобы починить машину', reply_markup=show_car_kb)
        elif car.energy <= 0:
            return await message.reply('⚡ У машины разрядился аккум(улятор), подождите немного чтобы он зарядился!')

        doxod = car.ride()
        return await message.reply(f'🏎️ Вы проехали {doxod[0]} км. и заработали {to_str(doxod[1])}'
                                   f' на счёт машины! (-1⚡) (-1⛽)\n'
                                   f'⚡ Текущая энергия: {car.energy}\n'
                                   f'⛽ Текущее состояние машины: {car.fuel}%', reply_markup=ride_car_kb)

    elif arg[0].lower() in ['починить', 'чинить', 'починка']:
        items = sql.execute(f'SELECT items FROM users WHERE id = {message.from_user.id}', False, True)[0][0]
        if '22:' not in items:
            return await message.reply('❌ У вас нет <b>Болтик 🔩</b> (x10) в инвентаре!',
                                       reply_markup=show_inv_kb)
        count = int(items.split('22:')[1].split(',')[0])
        if count < 10:
            return await message.reply(f'❌ Не хватает {10 - count} <b>Болтиков 🔩</b> для починки!',
                                       reply_markup=show_inv_kb)

        user_items = [[int(x.split(':')[0]), int(x.split(':')[1])] for x in items.split(',') if x]
        for index, i in enumerate(user_items):
            if i[0] == 22:
                break
        user_items[index] = [22, i[1] - 10]
        if (i[1] - 10) <= 0:
            user_items.remove(user_items[index])
        str_items = ','.join(f'{x[0]}:{x[1]}' for x in user_items if x)
        sql.executescript(f'UPDATE users SET items = "{str_items}" WHERE id = {message.from_user.id};\n'
                          f'UPDATE cars SET fuel = fuel + 1 WHERE id = {car.id};')

        return await message.reply('✅ Машина восстановлен на +1%')

    elif arg[0].lower() in ['оплата', 'оплатить', 'налог', 'налоги']:
        xd = car.nalog
        if len(arg) > 1:
            try:
                xd = get_cash(arg[1])
            except:
                pass
        if car.nalog < 1:
            return await message.reply('💲 Налог на машину и так оплачен!')
        elif car.nalog < xd:
            xd = car.nalog
        elif xd <= 0:
            return await message.reply('❌ Нельзя так!')
        if sql.execute(f'SELECT bank FROM users WHERE id = {message.from_user.id}', False, True)[0][0] < xd:
            return await message.reply(f'💲 Недостаточно денег в банке для оплаты налога, нужно: {to_str(xd)}!',
                                       reply_markup=show_balance_kb)

        sql.executescript(f'''UPDATE users SET bank = bank - {xd} WHERE id = {message.from_user.id};
                              UPDATE cars SET nalog = {car.nalog - xd} WHERE id = {car.id};''',
                          True)

        return await message.reply('✅ Налог на машину успешно оплачен!')
    else:
        return await message.reply('❌ Ошибка. Используйте: <code>Машина [снять|оплатить|ехать] *{сумма}</code>')
