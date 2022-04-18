import re
import time

from aiogram.types import Message

from config import bot_name
from keyboard.main import check_ls_kb
from utils.logs import readlogs, writelog
from utils.main.airplanes import Airplane
from utils.main.bitcoin import Bitcoin
from utils.main.businesses import Business
from utils.main.cars import Car
from utils.main.cash import to_str
from utils.main.chats import Chat
from utils.main.db import timetomin
from utils.main.houses import House
from utils.main.moto import Moto
from utils.main.rockets import Rocket
from utils.main.tanki import Tank
from utils.main.users import User
from utils.main.vertoleti import Vertolet
from utils.main.yaxti import Yaxta
from utils.marries import Marry


async def balance_handler(message: Message):
    arg = message.text.split()[1:] if not bot_name.lower() in message.text.split()[0].lower() else message.text.split()[2:]
    user = None
    if len(arg) > 0 and '@' in arg[0]:
        try:
            user = User(username=arg[0].replace('@', ''))
            if user.lock:
                return await message.reply('🔒 Кошелёк пользователя закрыт от других глаз!')
        except:
            user = User(user=message.from_user)
    if user is None:
        user = User(user=message.from_user)
    if len(arg) > 0 and arg[0].lower() == 'открыть':
        last = user.lock
        user.edit('lock', False)
        await message.reply(
            '🔓 Вы открыли свой кошелёк!' if last == True else '🔓 Ваш кошелёк и так был открыт!')
        await writelog(message.from_user.id, 'Открытие кошелька 🔓')
        return
    elif len(arg) > 0 and arg[0].lower() == 'закрыть':
        last = user.lock
        user.edit('lock', True)
        await message.reply(
            '🔒 Вы закрыли свой кошелёк!' if last == False else '🔒 Ваш кошелёк и так был закрыт!')
        await writelog(message.from_user.id, 'Закрытие кошелька 🔒')
        return

    await message.reply(text=user.text, disable_web_page_preview=True)

    if message.chat.id != message.from_user.id:
        Chat(chat=message.chat)


async def nickname_handler(message: Message):
    user = User(user=message.from_user)
    arg = ' '.join(message.text.split()[1:])
    args = re.sub(r'[^a-zA-Zа-яА-Я0-9]', '', arg)
    if not args:
        return await message.reply(f'👓 Ваш никнейм: <b>{user.name if user.name else user.first_name}</b>')
    else:
        if len(args) > 16 or len(args) < 4:
            return await message.reply('❌ Ошибка! Максимальная длина ника: 16, Минимальная: 6\n'
                                       'Также в никах разрешены только цифры, англ. и рус. буквы!')
        donate = user.donate
        args = args if not donate else donate.prefix + ' ' + args
        user.edit('name', args)
        await message.reply(f'✅ Ваш никнейм успешно изменён на: <code>{user.name}</code>')
        await writelog(message.from_user.id, 'Смена никнейма 👓')


last_use = {}


async def profile_handler(message: Message):
    if last_use.get(message.from_user.id):
        if time.time() - last_use[message.from_user.id] < 5:
            return await message.reply('❌ Вы недавно смотрели свой профиль!')
    last_use[message.from_user.id] = time.time()

    try:
        marry = Marry(user_id=message.from_user.id)
    except:
        try:
            marry = Marry(son=message.from_user.id)
        except:
            marry = None
    try:
        business = Business(user_id=message.from_user.id)
    except:
        business = None
    try:
        house = House(user_id=message.from_user.id)
    except:
        house = None
    try:
        car = Car(user_id=message.from_user.id)
    except:
        car = None
    try:
        tank = Tank(user_id=message.from_user.id)
    except:
        tank = None
    try:
        yaxta = Yaxta(user_id=message.from_user.id)
    except:
        yaxta = None
    try:
        vertolet = Vertolet(user_id=message.from_user.id)
    except:
        vertolet = None
    try:
        airplane = Airplane(user_id=message.from_user.id)
    except:
        airplane = None
    try:
        moto = Moto(user_id=message.from_user.id)
    except:
        moto = None
    try:
        rocket = Rocket(user_id=message.from_user.id)
    except:
        rocket = None
    try:
        btc = Bitcoin(owner=message.from_user.id)
    except:
        btc = None

    user = User(id=message.from_user.id)
    text = user.text
    text += '\n\n'
    xd = f' ({timetomin(int((int(user.energy_time) + 3600) - time.time()))})' if user.energy_time is not None else ''
    text += f'📅 Дата рег.: {user.reg_date}\n' \
            f'👥 Рефералы: {user.refs}\n' \
            f'🔒 Кошелёк: {"Закрыт" if user.lock else "Открыт"}\n' \
            f'⚡ Энергия: {user.energy}{xd}\n' \
            f'♟️ XP: {user.xp}\n' \
            f'🎫 Скидка: x{user.sell_count}\n' \
            f'⭐ BTC: <b>{btc.balance if btc else 0.0}</b>\n'
    try:
        text += f'⭐ Уровень: <b>{user.level_json.get("name")}</b>({user.level})\n'
    except:
        pass
    try:
        text += f'👻 Работа: <b>{user.job.get("name") if user.job else "Нет ❌"}</b>\n\n'
    except:
        pass

    text += f'💍 Семья: <b>{marry.name if marry and marry.name else "Есть ✅" if marry else "Нет ❌"}</b>\n' \
            f'👨‍💼 Бизнес: <b>{business.name if business else "Нет ❌"}</b>\n' \
            f'🏠 Дом: <b>{house.name if house else "Нет ❌"}</b>\n' \
            f'🏎️ Машина: <b>{car.name if car else "Нет ❌"}</b>\n' \
            f'🪖 Танк: <b>{tank.name if tank else "Нет ❌"}</b>\n' \
            f'🛳️ Яхта: <b>{yaxta.name if yaxta else "Нет ❌"}</b>\n' \
            f'🚁 Вертолёт: <b>{vertolet.name if vertolet else "Нет ❌"}</b>\n' \
            f'✈️ Самолёт: <b>{airplane.name if airplane else "Нет ❌"}</b>\n' \
            f'🏍️ Мото: <b>{moto.name if moto else "Нет ❌"}</b>\n' \
            f'🚀 Ракета: <b>{rocket.name if rocket else "Нет ❌"}</b>\n' \
            f'🎡 Ферма: <b>{btc.bitcoin.name if btc else "Нет ❌"}</b>\n'

    xd = [business, house, car, tank, yaxta,
                                  vertolet, airplane,
          moto, rocket, btc]
    nalog = sum(i.nalog for i in xd if i)

    text += f'💲 Налог в сумме: {to_str(nalog)}'

    try:
        await message.bot.send_message(chat_id=message.from_user.id,
                                       text=text,
                                       disable_web_page_preview=True)
        return await message.reply('✅ Я отправил ваш профиль, вам в личку!',
                                   reply_markup=check_ls_kb)
    except:
        return await message.reply('<b>😔 К сожалению я не могу отправить вам в личные сообщение ничего. Пожалуйста '
                                   'перейдите в лс с ботом @barleygamebot и нажмите /start</b>',
                                   disable_web_page_preview=True,
                                   reply_markup=check_ls_kb)


async def notifies_handler(message: Message):
    user = User(user=message.from_user)
    user.edit('notifies', not user.notifies)
    text = f'🔔 Статус уведомлений изменён на: {"Включены ✅" if user.notifies else "Выключены ❌"}'
    await message.reply(text=text)
    await writelog(message.from_user.id, 'Изменение уведомлений 🔔')


async def nedavno_handler(message: Message):
    text = await readlogs()
    lasts = [i.split(':') for i in text.split('\n') if i and len(i.split(':')) == 2].__reversed__()
    actions = []
    for user_id, action in lasts:
        user_id = int(user_id)
        if user_id == message.from_user.id:
            actions.append(action)
            if len(actions) >= 3:
                break
    return await message.reply(text=f'⏰ Ваши последние действия:\n\n'
                                    f'<code>{actions[0] if len(actions) > 0 else "Неизвестно"}</code>\n'
                                    f'➖➖➖➖➖➖➖➖➖\n'
                                    f'<code>{actions[1] if len(actions) > 1 else "Неизвестно"}</code>\n'
                                    f'➖➖➖➖➖➖➖➖➖\n'
                                    f'<code>{actions[2] if len(actions) > 2 else "Неизвестно"}</code>')
