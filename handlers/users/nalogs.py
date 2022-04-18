from aiogram.types import Message

from config import bot_name
from keyboard.main import nalogs_all_kb
from utils.logs import writelog
from utils.main.bitcoin import Bitcoin
from utils.main.cash import to_str
from utils.main.moto import Moto
from utils.main.rockets import Rocket
from utils.main.users import User
from utils.main.airplanes import Airplane
from utils.main.businesses import Business
from utils.main.cars import Car
from utils.main.houses import House
from utils.main.tanki import Tank
from utils.main.vertoleti import Vertolet
from utils.main.yaxti import Yaxta
from threading import Lock


lock = Lock()


async def nalogs_handler(message: Message):
    arg = message.text.split()[1:] if not bot_name.lower() in message.text.split()[0].lower() else message.text.split()[2:]
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

    xd = [business, house, car, tank, yaxta,
                                  vertolet, airplane,
          moto, rocket, btc]
    nalog = sum(i.nalog for i in xd if i)

    if len(arg) == 0:
        return await message.reply(f'💲 В сумме ваши налоги: {to_str(nalog)}\n\n'
                                   f'Введите: <code>Налоги оплатить</code> чтобы оплатить всё.',
                                   reply_markup=nalogs_all_kb)

    if nalog <= 0:
        return await message.reply('🤔 Все налоги и так оплачены.')

    user = User(user=message.from_user)
    if user.bank < nalog:
        return await message.reply(f'💲 Недостаточно денег в банке для оплаты налогов, нужно: {to_str(nalog)}')

    user.edit('bank', user.bank - nalog)

    for i in xd:
        if i and i.nalog > 0:
            with lock:
                i.edit('nalog', 0)

    await message.reply(f'⛄ Вы успешно оплатили все налоги ( {to_str(nalog)} )')
    await writelog(message.from_user.id, f'Оплата всех налогов')
    return


async def autonalog_handler(message: Message):
    arg = message.text.split()[1:] if not bot_name.lower() in message.text.split()[0].lower() else message.text.split()[2:]
    user = User(user=message.from_user)
    if user.autonalogs:
        x1, x2 = 'Включены ☑️', 'выключить'
    else:
        x1, x2 = 'Выключены 🚫', 'включить'
    if len(arg) == 0:
        return await message.reply(f'😃 Ваш статус авто-налогов: <b>{x1}</b>\n'
                                   f'📢 Введите: <code>Автоналоги {x2}</code> чтобы {x2} их.')
    elif arg[0].lower().startswith('вкл'):
        now = True
        x1, x2 = 'Включены ☑️', 'выключить'
        user.edit('autonalogs', now)
        return await message.reply(f'Авто-налоги были успешно {x1}\n'
                                   f'📢 Введите: <code>Автоналоги {x2}</code> чтобы {x2} их.')

    elif arg[0].lower().startswith('выкл'):
        now = False
        x1, x2 = 'Выключены 🚫', 'включить'
        user.edit('autonalogs', now)
        return await message.reply(f'Авто-налоги были успешно {x1}\n'
                                   f'📢 Введите: <code>Автоналоги {x2}</code> чтобы {x2} их.')
    else:
        return await message.reply(f'😃 Ваш статус авто-налогов: <b>{x1}</b>\n'
                                   f'📢 Введите: <code>Автоналоги {x2}</code> чтобы {x2} их.')
