import random

from aiogram.types import Message

from utils.logs import writelog
from utils.main.cash import to_str
from utils.main.users import User
from utils.pets.pets import pets
from utils.photos.photos import get_photo, set_photo


async def pets_handler(message: Message):
    arg = message.text.split()[1:]
    if len(arg) == 0:
        t = '\n'.join(f'<code>{index}</code> • <b>{i["name"]} {i["emoji"]}</b> — {to_str(i["price"])}' for index,
                                                                                                           i in
                      pets.items())
        return await message.reply(text=f'🐇 Список питомцев для покупки:\n\n'
                                        + t + '\n\n✅ Введите: <code>pet купить '
                                              '{номер}</code> чтобы купить '
                                              'питомца')

    user = User(user=message.from_user)
    user.pets = list(user.pets)

    if arg[0].lower() == 'купить':
        try:
            index = int(arg[1])
            if index not in pets:
                raise Exception('132')
        except:
            return await message.reply('❌ Ошибка. Неверно введёт номер питомца!')
        pet = pets[index]
        if user.balance < pet['price']:
            return await message.reply('💸 Недостаточно средств!')
        user.pets.append(index)
        corm = random.randint(1, 5)
        user.editmany(balance=user.balance - pet['price'], pets=','.join(str(x) for x in user.pets))
        user.items = list(user.items)
        user.set_item(item_id=1, x=corm)
        msg = await message.reply_photo(photo=get_photo(f'pets/{index}'),
                                        caption=f'✅ Вы успешно купили питомца <b>{pet["name"]} {pet["emoji"]}'
                                                f' (<code>x1</code>)</b>\n'
                                                f'🥜 В добавок получили (<code>x{corm}</code>) пачек корма!')
        set_photo(f'pets/{index}', msg.photo[-1].file_id)
        await writelog(message.from_user.id, f'Покупка питомца <b>{pet["name"]} {pet["emoji"]}</b>')
        return
    elif arg[0].lower() == 'мои':
        text = '🐇 Ваши питомцы: \n\n'
        completed = []
        for index, i in enumerate(user.pets, start=1):
            if i in completed:
                continue
            completed.append(i)
            text += f'<code>{index}</code> • <b>{pets[i]["name"]} (<code>x{user.pets.count(i)}</code>) ' \
                    f'{pets[i]["emoji"]}</b>'
        if text == '🐇 Ваши питомцы: \n\n':
            return await message.reply('🐇 У тебя нет питомцев! :(')
        return await message.reply(text=text)
    elif arg[0].lower() == 'продать':
        try:
            index = int(arg[1])
            if index < 1:
                raise Exception('1')
        except:
            return await message.reply('❌ Ошибка. Неверно введёт номер питомца!')
        if index > len(user.pets):
            return await message.reply('❌ Ошибка. У вас нет этого питомца!')
        xd = user.pets[index - 1]
        pet = pets[xd]
        user.pets.remove(xd)
        user.editmany(balance=user.balance + int(pet['price'] // 1.5), pets=','.join(str(x) for x in user.pets))
        msg = await message.reply_photo(
            photo=get_photo(f'pets/{xd}'),
            caption=f'✅ Вы успешно продали питомца '
                    f'<b>{pet["name"]} {pet["emoji"]} (<code>x1</code>)</b> и получили '
                    f'+{to_str(int(pet["price"] // 1.4))}')
        set_photo(f'pets/{xd}', msg.photo[-1].file_id)
        await writelog(message.from_user.id, f'Продажа питомца <b>{pet["name"]} {pet["emoji"]}</b>')
        return
    else:
        return await message.reply('❌ Ошибка. Используйте: <code>питомцы [купить|мои|продать] {<i>номер</i>}</code>')
