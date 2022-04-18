import time

from aiogram.types import Message

from config import bot_name
from utils.logs import writelog
from utils.main.cash import to_str, get_cash
from utils.main.users import User


async def deposit_handler(message: Message):
    spliy = message.text.split() if not bot_name.lower() in message.text.split()[0].lower() else message.text.split()[1:]
    user = User(user=message.from_user)
    try:
        arg = abs(get_cash(spliy[2].lower().replace('всё', str(user.deposit)).replace('все', str(user.deposit)))) if spliy[
                                                                                                                   1].lower() in [
                                                                                                                   'снять',
                                                                                                                   'вывести',
                                                                                                                   'обналичить'] else abs(
            get_cash(
                spliy[2].lower().replace('всё', str(user.balance)).replace('все', str(user.balance))))
        if arg <= 0:
            raise Exception(123)
    except:
        return await message.reply(f'❌ Ошибка! Неверный аргумент, введите: <code>депозит [снять|пополнить|вывести] {{ '
                                   f'сумма }}</code>')
    if spliy[1].lower() in ['положить', 'пополнить', 'внести']:
        if user.balance < arg:
            return await message.reply('💸 На руках недостаточно средств, чтобы пополнить такую сумму на депозит!')
        user.editmany(balance=user.balance - arg, deposit=user.deposit + arg, deposit_date=time.time())
        await message.reply(f'✅ Вы пополнили баланс депозита на +{to_str(arg)}, текущий баланс на депозите: '
                                   f'{to_str(user.deposit)}')
        await writelog(message.from_user.id, f'Депозит +{to_str(arg)}')
        return
    elif spliy[1].lower() in ['снять', 'вывести', 'обналичить']:
        if user.deposit < arg:
            return await message.reply('💶 На депозите недостаточно средств, чтобы снять средства!')
        user.editmany(balance=user.balance + arg, deposit=user.deposit - arg, deposit_date=time.time())
        await message.reply(f'✅ Вы сняли средства в размере {to_str(arg)} и теперь у вас на руках '
                                   f'{to_str(user.balance)}')
        await writelog(message.from_user.id, f'Депозит -{to_str(arg)}')
        return
    return await message.reply(f'❌ Ошибка! Неверный аргумент, введите: <code>деп [снять|пополнить|вывести] {{ '
                               f'сумма }}</code>')
