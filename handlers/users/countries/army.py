from aiogram.types import Message

from config import bot_name
from utils.countries import Country, tech_price, snaraj_price, rockets_price
from keyboard.countries import army_kb
from utils.main.cash import to_str


async def army_handler(message: Message):
    country = Country.get_by_user(message.from_user.id)
    if country.owner != message.from_user.id:
        return await message.reply('😐 Вы не президент страны!')

    text = country.army.text
    return await message.reply(text=text, reply_markup=army_kb)


async def army_tech_handler(message: Message):
    arg = message.text.split() if not bot_name.lower() in message.text.split()[0].lower() else message.text.split()[1:]
    country = Country.get_by_user(message.from_user.id)
    if country.owner != message.from_user.id:
        return await message.reply('😐 Вы не президент страны!')

    try:
        arg = int(arg[2])
    except:
        return await message.reply('⛔ Используйте: <code>Армия техника {кол-во}</code> чтобы купить технику')

    if arg < 1:
        return await message.reply('⛔ Количество техники должно быть больше 0')

    price = tech_price * (country.army.tech + arg)

    if price > country.balance:
        return await message.reply('⛔ Недостаточно средств в бюджете страны для покупки техники.\n'
                                   f'Нужно: {to_str(price)}')

    country.army.edit('tech', country.army.tech + arg
                      )
    country.editmany(balance=country.balance - price)
    return await message.reply(f'✅ Техника в кол-ве <code>x{arg}</code> за {to_str(price)} была куплена в страну '
                               f'{country.full_name}')


async def army_snaraj_handler(message: Message):
    arg = message.text.split() if not bot_name.lower() in message.text.split()[0].lower() else message.text.split()[1:]

    country = Country.get_by_user(message.from_user.id)
    if country.owner != message.from_user.id:
        return await message.reply('😐 Вы не президент страны!')

    try:
        arg = int(arg[2])
    except:
        return await message.reply('⛔ Используйте: <code>Армия снаряжение {кол-во}</code> чтобы купить снаряжение')

    if arg < 1:
        return await message.reply('⛔ Количество снаряжения должно быть больше 0')

    price = snaraj_price * (country.army.tech + arg)

    if price > country.balance:
        return await message.reply('⛔ Недостаточно средств в бюджете страны для покупки снаряжения.\n'
                                   f'Нужно: {to_str(price)}')

    country.army.edit('snaraj', country.army.snaraj + arg
                          )
    country.editmany(balance=country.balance - price)
    return await message.reply(f'✅ Снаряжение в кол-ве <code>x{arg}</code> за {to_str(price)} былo куплена в страну '
                               f'{country.full_name}')


async def army_rockets_handler(message: Message):
    arg = message.text.split() if not bot_name.lower() in message.text.split()[0].lower() else message.text.split()[1:]

    country = Country.get_by_user(message.from_user.id)
    if country.owner != message.from_user.id:
        return await message.reply('😐 Вы не президент страны!')

    try:
        arg = int(arg[2])
    except:
        return await message.reply('⛔ Используйте: <code>Армия ракеты {кол-во}</code> чтобы купить ракеты')

    if arg < 1:
        return await message.reply('⛔ Количество ракет должно быть больше 0')

    price = rockets_price * (country.army.tech + arg)

    if price > country.balance:
        return await message.reply('⛔ Недостаточно средств в бюджете страны для покупки ракет.\n'
                                   f'Нужно: {to_str(price)}')

    country.army.edit('rockets', country.army.rockets + arg
                      )
    country.editmany(balance=country.balance - price)
    return await message.reply(f'✅ Ракеты в кол-ве <code>x{arg}</code> за {to_str(price)} были куплены в страну '
                               f'{country.full_name}')


async def army_gotov_handler(message: Message):
    country = Country.get_by_user(message.from_user.id)
    if country.owner != message.from_user.id:
        return await message.reply('😐 Вы не президент страны!')

    now = not country.army.status
    country.army.edit('status', now)
    if now:
        return await message.reply('⛔ Армия была переведа в состояние готовности!')
    else:
        return await message.reply('✅ Армия была переведа в состояние отдыха!')
