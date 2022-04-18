import asyncio
from datetime import datetime, timedelta

from aiogram.dispatcher import FSMContext
from aiogram.types import Message, InputFile, InlineKeyboardMarkup, InlineKeyboardButton

from config import donates
from keyboard.main import admin_kb, cancel, remove
from states.admins import ABD
from utils.main.airplanes import all_airplanes
from utils.main.businesses import all_businesses
from utils.main.cars import all_cars
from utils.main.chats import all_chats, Chat
from utils.main.db import sql
from utils.main.houses import all_houses
from utils.main.moto import all_moto
from utils.main.tanki import all_tanki
from utils.main.users import User, all_users, timetomin
from utils.main.cash import to_str, get_cash
from utils.main.donates import to_str as to_strs
import os
import psutil
from threading import Lock

from utils.main.vertoleti import all_vertoleti
from utils.main.yaxti import all_yaxti
from utils.marries import all_marries
from utils.promo.promo import all_promo

lock = Lock()


async def givebalance_handler(message: Message):
    arg = message.text.split()[1:]

    if len(arg) < 1:
        return await message.reply('Используйте: <code>Выдать {сумма} *{ссылка}')

    summ = get_cash(arg[0])
    arg[0] = arg[0].replace('$', '')
    if len(arg) > 1:
        to_user = User(username=arg[1].replace('@', ''))
    else:
        to_user = User(user=message.reply_to_message.from_user)
    if arg[0][0] == '+':
        summ = to_user.balance + summ
    elif arg[0][0] == '-':
        summ = to_user.balance + summ

    to_user.edit('balance', summ)

    return await message.reply(f'Вы успешно выдали пользователю {to_user.link} {to_str(summ)} и его теку'
                               f'щий баланс: {to_str(summ)}',
                               disable_web_page_preview=True)


async def givebalance_admin_handler(message: Message):
    arg = message.text.split()[1:]
    if len(arg) == 0:
        return await message.reply('Используйте: <code>Выдать {кол-во} *{ссылка}</code>')
    now = datetime.now()
    user = User(user=message.from_user)
    if user.admin_last is not None:
        x = (now - user.admin_last).total_seconds()
    else:
        x = 3600
    if x < 3600:
        return await message.reply(f'💓 Вы можете выдавать раз в час, след. через: {timetomin(x)}')

    try:
        summ = get_cash(arg[0])
        if summ > 50000000:
            return await message.reply('Максимум <code>$50,000,000</code>!')
        if len(arg) > 1:
            to_user = User(username=arg[1].replace('@', ''))
        else:
            to_user = User(user=message.reply_to_message.from_user)
        summ = to_user.balance + summ

        sql.executescript(f'UPDATE users SET balance = balance + {summ} WHERE id = {to_user.id};\n'
                          f'UPDATE users SET admin_last = "{now.strftime("%d-%m-%Y %H:%M:%S")}" WHERE id = {user.id}',
                          True, False)

        return await message.reply(f'Вы успешно выдали пользователю {to_user.link} {to_str(summ)} и его теку'
                                   f'щий баланс: {to_str(summ)}',
                                   disable_web_page_preview=True)
    except:
        return await message.reply('Шота ни так, попробуй заново')


async def givedonate_handler(message: Message):
    arg = message.text.split()[1:]

    if len(arg) < 1:
        return await message.reply('Используйте: <code>Ддонат {сумма} *{ссылка}')

    summ = get_cash(arg[0])
    arg[0] = arg[0].replace('$', '')
    if len(arg) > 1:
        to_user = User(username=arg[1].replace('@', ''))
    else:
        to_user = User(user=message.reply_to_message.from_user)
    if arg[0][0] == '+':
        summ = to_user.coins + summ
    elif arg[0][0] == '-':
        summ = to_user.coins + summ

    to_user.edit('coins', summ)

    return await message.reply(f'Вы успешно выдали пользователю {to_user.link} {summ} и его теку'
                               f'щий донатный баланс: {to_str(summ)}',
                               disable_web_page_preview=True)


async def privilegia_handler_admin(message: Message):
    arg = message.text.split()[1:]
    if 'vip' in arg[0].lower() or 'вип' in arg[0].lower():
        priva = 1
    elif 'prem' in arg[0].lower() or 'прем' in arg[0].lower():
        priva = 2
    elif 'адм' in arg[0].lower() or 'adm' in arg[0].lower():
        priva = 3
    elif '0' in arg[0] or 'игрок' in arg[0].lower():
        priva = None
    elif 'код' in arg[0].lower():
        priva = 4
    elif 'уни' in arg[0].lower():
        priva = 5
    else:
        return await message.reply('❌ Такой привилегии не существует!')

    if len(arg) > 1:
        user = User(username=arg[1].replace('@', ''))
    else:
        user = User(user=message.reply_to_message.from_user)

    if priva is not None:
        item = donates[priva]
        x = f'{priva},{datetime.now().strftime("%d-%m-%Y %H:%M")}'
    else:
        item = {'name': 'Игрок', 'price': 0}
        x = None

    user.editmany(donate_source=x)

    return await message.reply(f'✅ Вы успешно выдали привилегию <b>{item["name"]}</b> за {item["price"]}🪙 '
                               f'пользователю {user.link}',
                               disable_web_page_preview=True)


stats_text = 'Ошибочка, ээээээээ!'


async def stats_handler(message: Message):
    load1, load5, load15 = psutil.getloadavg()

    cpu_usage = round((load15 / os.cpu_count()) * 100, 2)

    total_memory, used_memory, free_memory = map(
        int, os.popen('free -t -m').readlines()[-1].split()[1:])

    ram_usage = round((used_memory / total_memory) * 100, 2)

    global stats_text
    stats_text = f'⛵ Яхты: {len(all_yaxti())}\n' \
                 f'🚁 Вертолёты: {len(all_vertoleti())}\n' \
                 f'🪖 Танки: {len(all_tanki())}\n' \
                 f'🏠 Дома: {len(all_houses())}\n' \
                 f'🏎️ Машины: {len(all_cars())}\n' \
                 f'🧑‍💼 Бизнеса: {len(all_businesses())}\n' \
                 f'✈️ Самолёты: {len(all_airplanes())}\n' \
                 f'🏍️ Мотоциклы: {len(all_moto())}\n\n'

    lent = sum([len(all_yaxti()), len(all_vertoleti()),
                len(all_tanki()), len(all_houses()),
                len(all_cars()), len(all_businesses()),
                len(all_airplanes()), len(all_moto())])

    text = f'👥 Пользователей в боте: {len(all_users())}\n' \
           f'💭 Чатов добавило бота: {len(all_chats())}\n\n' \
           f'🙉 Промокодов: {len(all_promo())}\n' \
           f'👨‍👩‍👦 Семьи: {len(all_marries())}\n' \
           f'📃 Имущество: <b>{lent}</b>\n➖\n' \
           f'⚙️ CPU usage: {cpu_usage}%\n' \
           f'🔩 RAM usage: {ram_usage}%'

    kb = admin_kb
    if message.chat.id != message.from_user.id:
        kb = InlineKeyboardMarkup(row_width=1)
        kb.add(InlineKeyboardButton(text='Инфа о имуществе ➖', callback_data='statsdop'))

    return await message.reply(text, reply_markup=kb)


async def stats_dop_call(call):
    try:
        kb = admin_kb
        if call.message.chat.id != call.message.from_user.id:
            kb = InlineKeyboardMarkup(row_width=1)
            kb.add(InlineKeyboardButton(text='Инфа о имуществе ➖', callback_data='statsdop'))

        return await call.message.edit_text(call.message.text.replace('➖', stats_text),
                                            reply_markup=kb)
    except:
        return


async def get_chat_list(call):
    chats = [Chat(source=i) for i in sql.get_all_data('chats')]
    text = f'📃 Список чатов:\n\n'
    for index, chat in enumerate(chats, start=1):
        link = f'@{chat.username}' if chat.username else f'<a href="{chat.invite_link}">Invite*</a>'
        text += f'''{index}. <b>{chat.title}</b> - {link}\n'''
    return await call.message.answer(text)


async def plan_bd(call):
    await call.message.answer_document(document=InputFile('assets/database.db'),
                                       caption=f'База за {datetime.now()}\n\n'
                                               f'Введите запрос который должен выполниться:',
                                       reply_markup=cancel)
    await ABD.start.set()


async def plan_bd_step1(message: Message, state: FSMContext):
    await ABD.next()
    await state.update_data(query=message.text)
    return await message.reply('🎄 Введите через сколько выполнить запрос (дата) или "-" если сейчас:',
                               reply_markup=cancel)


async def plan_bd_step2(message: Message, state: FSMContext):
    await ABD.next()
    await state.update_data(text=message.text)
    return await message.reply('🎄 Введите нужен ли коммит (+ или -):',
                               reply_markup=cancel)


async def plan_bd_finish(message: Message, state: FSMContext):
    data = await state.get_data()
    text = data['text']
    query = data['query']
    commit = True if '+' in message.text else False
    await state.finish()

    if text == '-':
        time = 'сейчас'
        seconds = 0
    else:
        now = datetime.now()
        if '.' not in text:
            text = f'{now.day}.{now.month}.{now.year} ' + text
        time = datetime.strptime(text, '%d.%m.%Y %H:%M')
        seconds = (time - now).total_seconds()

    msgs = await message.reply(reply_markup=remove,
                               text=f'🍿 Успешно запланировано на {time}!')

    await asyncio.sleep(seconds)

    with lock:
        sql.execute(query=query, commit=commit, fetch=False)

    return await msgs.reply('🍿 Запрос был успешно выполнен!')
