import random
import time

from aiogram.types import Message

from config import bot_name
from keyboard.jobs import jobs_kb
from utils.jobs.jobs import jobs, levels
from utils.logs import writelog
from utils.main.cash import to_str
from utils.main.db import timetostr
from utils.main.users import User


async def jobs_handler(message: Message):
    user = User(user=message.from_user)
    if user.job_time is None and user.work_time is None:
        user.editmany(job_time=time.time(),
                      work_time=time.time())
    elif user.job_time is None:
        user.edit('job_time', time.time())
    elif user.work_time is None:
        user.edit('work_time', time.time())

    arg = message.text.split()[1:] if not bot_name.lower() in message.text.split()[0].lower() else message.text.split()[2:]

    if len(arg) == 0:
        text = f'' \
               f'Ваша работа: <b>{user.job.name if user.job else "Нет."}</b>\n' \
               f'Ваш уровень: <b>{user.level_json["name"]} ({user.level})</b>\n' \
               f'➖➖➖➖➖➖➖➖➖➖➖➖\n' \
               f'💲 Доход/час: {to_str(user.job.doxod if user.job else user.level_json["doxod"])}\n' \
               f'⌚ Следующее повышение через: (<code>{timetostr(int(user.job_time + 3600*12 - time.time()))}</code>)'

        return await message.reply(text, reply_markup=jobs_kb)

    x = ' '.join(arg)
    if 'взятк' in x.lower():
        if user.level <= 1:
            return await message.reply('❌ Ошибка. Слишком маленький уровень для взяток!')
        elif user.balance < 10000 * (user.level+1):
            return await message.reply(f'💲 Вам нужно {to_str(10000*(user.level+1))} чтобы дать взятку!')
        xd = random.randint(1, 10)

        if xd == 5:
            user.editmany(balance=user.balance - 10000 * (user.level + 1),
                          level=user.level - 1)
            name = levels[user.level]["name"] if user.level < 13 else levels[12]['name']
            return await message.reply(f'❌ Вас поймали с поличным и вы были понижены до <b>{name} ({user.level})</b>\n'
                                       f'С баланса было списано: -{to_str(10000 * (user.level + 1))}')
        user.editmany(balance=user.balance - 10000 * (user.level + 1),
                      level=user.level+1)
        name = levels[user.level]["name"] if user.level < 13 else levels[12]['name']
        await message.reply(f'✅ Вы повысились до уровня <b>{name} ({user.level})</b>\nС баланса было списано: -{to_str(10000 * (user.level + 1))}')
        await writelog(message.from_user.id, f'Взятка на работе')
        return
    elif arg[0]:
        if len(arg) >= 2:
            if user.level < 12:
                return await message.reply(f'🕯️ Ваш уровень <b>{user.level_json["name"]} ({user.job_index})</b>, а нужен:'
                                           f' <b>Жизнь ❤️‍🩹 (12)</b>')
            try:
                number = int(arg[1])
                if number <= 0 or number > len(jobs):
                    raise Exception('123')
            except:
                return await message.reply('❌ Ошибка. Неверно введён номер профессии!')

            job = jobs[number]
            if job['level'] > user.level:
                return await message.reply(f'❌ Ваш уровень меньше чем нужен для профессии! Нужен: {job["level"]}')

            user.edit('job_index', number)
            await message.reply(f'🕯️ Вы устроились на работу: <b>{job["name"]}</b> и теперь ваш доход '
                                       f'{to_str(job["doxod"])}')
            await writelog(message.from_user.id, f'Смена работы на {job["name"]}')
            return
        else:
            text = '👨‍🦳 Список всех профессий:\n' \
                   '<i>Номер. Название (лвл) - доход</i>\n\n'
            for index, job in jobs.items():
                text += f'<code>{index}</code>. {job["name"]} ({job["level"]}) - {job["doxod"]}\n'

            return await message.reply(text=text)
