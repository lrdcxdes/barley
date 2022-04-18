import asyncio
import numpy as np
from aiogram.dispatcher import FSMContext
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from datetime import datetime
from keyboard.main import cancel, remove
from states.admins import Rass
from utils.main.users import all_users
from utils.main.chats import all_chats


async def rass_menu_handler(call: CallbackQuery, state: FSMContext):
    await Rass.post.set()
    await state.update_data(action=call.data.split('_')[1])
    return await call.message.answer('📃 Пришлите мне сообщение для рассылки:', reply_markup=cancel)


async def rass_step2_handler(message: Message, state: FSMContext):
    await Rass.next()
    await state.update_data(msg=message)
    return await message.answer('🎙️ Клавиатура (name|btn, name|btn\\n) или "-" чтобы пропустить',
                                reply_markup=cancel)


async def rass_step3_handler(message: Message, state: FSMContext):
    await Rass.next()
    if message.text != '-':
        text = message.text.split('\n')
        lenght = len(text[0].split(','))
        kb = InlineKeyboardMarkup(row_width=lenght)
        for i in text:
            i = i.split(',')
            for z in i:
                name, url = z.split('|')
                kb.insert(InlineKeyboardButton(text=name, url=url))
    else:
        kb = None
    await state.update_data(kb=kb)
    return await message.answer('📅 Пришлите мне дату в формате (d.m.Y h:m) или "-" чтобы пропустить',
                                reply_markup=cancel)


async def rass_finish_handler(message: Message, state: FSMContext):
    data = await state.get_data()
    await state.finish()
    text = message.text
    if text == '-':
        time = 'сейчас'
        seconds = 0
    else:
        now = datetime.now()
        if '.' not in text:
            text = f'{now.day}.{now.month}.{now.year} ' + text
        time = datetime.strptime(text, '%d.%m.%Y %H:%M')
        seconds = (time - now).total_seconds()

    await message.answer(text=f'❤️ Рассылка была запланирована на {time}', reply_markup=remove)

    await asyncio.sleep(seconds)

    part0, part1, part2 = np.array_split(all_users() if data['action'] == 'users' else all_chats(), 3)

    m = await message.answer('Отправлено: 0\n'
                             'Успешно: 0\n'
                             'Неуспешно: 0')

    index = 0
    allow, decline = 0, 0

    msg = data['msg']
    kb = data['kb']

    for user_id in part0:
        index += 1
        try:
            await msg.send_copy(chat_id=user_id,
                                reply_markup=kb)
            allow += 1
        except:
            decline += 1

    await m.edit_text(f'Отправлено: {index}\n'
                      f'Успешно: {allow}\n'
                      f'Неуспешно: {decline}')

    for user_id in part1:
        index += 1
        try:
            await msg.send_copy(chat_id=user_id,
                                reply_markup=kb)
            allow += 1
        except:
            decline += 1

    await m.edit_text(f'Отправлено: {index}\n'
                      f'Успешно: {allow}\n'
                      f'Неуспешно: {decline}')

    for user_id in part2:
        index += 1
        try:
            await msg.send_copy(chat_id=user_id,
                                reply_markup=kb)
            allow += 1
        except:
            decline += 1

    await m.edit_text(f'Отправлено: {index}\n'
                      f'Успешно: {allow}\n'
                      f'Неуспешно: {decline}\n\n'
                      f'Завершено!')
