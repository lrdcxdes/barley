import random
import time
from datetime import datetime

from aiogram.types import Message
from random import choices, randint

from utils.main.cash import to_str
from utils.main.db import timetostr, timetomin
from utils.main.users import User

dbonus = {
    'vip': 55,
    'premium': 60,
    'admin': 65,
    1: 55,
    2: 60,
    3: 65
}


class Rob:
    @staticmethod
    def rob(ow: User, user: User):
        if user.donate or user.shield_count > 0:
            if user.shield_count > 0:
                user.edit('shield_count', user.shield_count - 1)
            return False
        r = user.balance // 4
        if r > 25000000:
            r = random.randint(0, 25000000)
        else:
            r = random.randint(0, int(user.balance // 4))
        if ow.donate:
            chance = dbonus[ow.donate.id]
        else:
            chance = 50
        cash = random.choices([+r, 0, -r], weights=(chance, 50, 50), k=1)[0]
        if cash > 0:
            user.edit('balance', user.balance - cash)
        return cash

    def __init__(self, name: str, price_range: tuple):
        self.name = name
        self.price_range = price_range

    def press(self, donate: str = None):
        if donate:
            chance = dbonus[donate]
        else:
            chance = 50
        summ = randint(*self.price_range)
        result = choices([+summ, 0, -summ], weights=(chance, 50, 50), k=1)[0]
        return result


robs = {
    Rob('Мэрия 🏢', (45000, 100000)): lambda txt: True in [i in txt for i in [
        'мерия', 'мэрия',
        'мериа', 'мерию',
        'мэрию', 'мериу']],
    Rob('Банк 🏦', (50000, 1500000)): lambda txt: True in [i in txt for i in [
        'банк',
        'bank',
        'бэнк',
        'бпнк'
    ]],
    Rob('Офис Президента 😶‍🌫️', (1000000, 5000000)): lambda txt: True in [i in txt for i in [
        'офис',
        'президент',
        'президента',
        'презика'
    ]]
}


async def rob_func(message):
    user = User(user=message.from_user)
    if (time.time() - user.last_rob) < 7200:
        xd = int(time.time() - user.last_rob)
        xa = str(xd / 3600).split('.')
        x = '1ч ' + timetomin(xd) if xa[0] == '2' or int(xa[1]) > 0 else timetomin(xd)
        return await message.reply(f'⌛ Подождите ещё <code>{x}</code> до повторной возможности грабить!')
    if message.reply_to_message.from_user.id == message.from_user.id:
        return await message.reply('❌ Нельзя так...')
    cash = Rob.rob(user, User(user=message.reply_to_message.from_user))
    if cash is False:
        user.edit('last_rob', time.time())
        return await message.reply('🛡️ Не удалось ограбить пользователя, так как у него был щит или '
                                   'привилегия!')
    elif cash == 0:
        user.edit('last_rob', time.time())
        return await message.reply('🧛🏿 Вы попытались ограбить пользователя и у вас не получилось, но так как '
                                   'вы успели убежать, то у вас ничего не отобрали!')
    elif cash < 0:
        user.editmany(last_rob=time.time(),
                      balance=user.balance + cash)
        return await message.reply('🧛🏿 Вы попытались ограбить пользователя и у вас не получилось, но так как '
                                   f'вы НЕ успели убежать, то у вас отобрали: {to_str(cash)}')
    elif cash > 0:
        user.editmany(last_rob=time.time(),
                      balance=user.balance + cash)
        return await message.reply(f'🧛🏿 Вы успешно ограбили пользователя и получили: {to_str(cash)}. Быстрее '
                                   f'убегайте!!!')


async def rob_handler(message: Message):
    arg = message.text.split()[1:] if message.text.split()[0].lower() != 'продать' else message.text.split()
    if len(arg) == 0:
        if not message.reply_to_message:
            return await message.reply('🍬 Используйте: <code>Ограбить {ссылка или название заведения}</code>')
        else:
            return await rob_func(message)
    else:
        if message.reply_to_message:
            if message.reply_to_message.from_user.id == message.from_user.id:
                return await message.reply('❌ Нельзя так...')
            return await rob_func(message)
        else:
            user = User(user=message.from_user)
            if (time.time() - user.last_rob) < 7200:
                xd = int(time.time() - user.last_rob)
                xa = str(xd / 3600).split('.')
                x = '1ч ' + timetomin(xd) if xa[0] == '2' or int(xa[1]) > 0 else timetomin(xd)
                return await message.reply(f'⌛ Подождите ещё <code>{x}</code> до повторной возможности грабить!')

            name = arg[0].lower()
            item = None
            for item, func in robs.items():
                if func(name):
                    break
            if item is None:
                return await message.reply('❌ Такого заведения не существует!')
            cash = item.press()
            if cash == 0:
                user.edit('last_rob', time.time())
                return await message.reply(f'🧛🏿 Вы попытались ограбить {item.name} и у вас не получилось, но так как '
                                           'вы успели убежать, то у вас ничего не отобрали!')
            elif cash < 0:
                user.editmany(last_rob=time.time(),
                              balance=user.balance + cash)
                return await message.reply(f'🧛🏿 Вы попытались ограбить {item.name} и у вас не получилось, но так как '
                                           f'вы НЕ успели убежать, то у вас отобрали: {to_str(cash)}')
            elif cash > 0:
                user.editmany(last_rob=time.time(),
                              balance=user.balance + cash)
                return await message.reply(f'🧛🏿 Вы успешно ограбили {item.name} и получили: {to_str(cash)}. Быстрее '
                                           f'убегайте!!!')


async def shield_handler(message: Message):
    arg = message.text.split()[1:] if message.text.split()[0].lower() != 'продать' else message.text.split()
    user = User(user=message.from_user)
    if len(arg) == 0:
        return await message.reply(f'<b>🛡️ Кол-во ваших щитов:</b> <code>{user.shield_count}</code>\n\n'
                                   'Введите: <code>Щит *{кол-во}</code> чтобы купить щит!')
    else:
        try:
            count = int(arg[0])
        except:
            count = 1
        price = 250000 * count
        if user.balance < price:
            return await message.reply(f'💲 Для покупки {count} щит(а) нужно: {to_str(price)}')
        user.editmany(shield_count=user.shield_count + count, balance=user.balance - price)
        return await message.reply(f'🛡️ Вы успешно купили {count} щит(ов) за {to_str(price)}!\n\n'
                                   f'Теперь вас никто не ограбит {count} раз :)')
