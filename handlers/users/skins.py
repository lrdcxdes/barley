from aiogram.types import Message, CallbackQuery, InputMediaPhoto, InputMedia

from config import bot_name
from utils.main.cash import to_str
from utils.main.users import User
from keyboard.skins import skin_buy_kb, skin_kb
from utils.photos.photos import set_photo, get_photo


class Skin:
    def __init__(self, name: str, price: int, ids: int, sex: str):
        self.id = ids
        self.name = name
        self.price = price
        self.img = 'skins/' + str(self.id)
        self.sex = sex

    def image(self, fide: str = ''):
        if fide:
            fide = '_' + fide
        return get_photo(self.img + fide + '.png')

    def set_image(self, value, fide: str = ''):
        if fide:
            fide = '_' + fide
        set_photo(self.img + fide + '.png', value)

    @property
    def text(self):
        return f'🔢 Номер скина: <code>{self.id}</code>\n' \
               f'👔 Название скина: <b>{self.name}</b>\n' \
               f'💰 Цена: {to_str(self.price)}'


skins = {
    1: Skin('Noel', 165000, 1, 'girl'),
    2: Skin('Amber', 2500000, 2, 'girl'),
    3: Skin('Annie', 5000000, 3, 'girl'),
    4: Skin('Rikka', 10000000, 4, 'girl'),
    5: Skin('RinTohsaka', 20000000, 5, 'girl'),
}

girls = [1, 2, 3, 4, 5]
boys = []


async def skins_handler(message: Message):
    arg = message.text.split()[1:] if not bot_name.lower() in message.text.split()[0].lower() else message.text.split()[2:]
    user = User(user=message.from_user)
    if (not user.skin and len(arg) == 0) or (len(arg) == 1 and arg[0].lower() in ['скины', 'все',
                                                                                    'список', 'купить']) or (len(arg)
                                == 1 and arg[0].lower() in ['girl', 'girls', 'тян', 'тяночки',
                                                            'тянки', 'девки', 'девка', 'девочки',
                                                            'девушки', 'женщины',
                                                            'boys', 'boy', 'кун', 'кунчики',
                                                            'мальчики', 'пацаны', 'мужики',
                                                            'парни']):
        text = '👘 Список доступных скинов:\n\n'
        x = boys if len(arg) >= 1 and arg[0].lower() in ['boys', 'boy', 'кун', 'кунчики',
                                                          'мальчики', 'пацаны', 'мужики',
                                                          'парни'] else girls
        skinss = [(i, skins[i]) for i in x]
        index = None
        for index, skin in skinss:
            text += f'{index}. <b>{skin.name}</b> - {to_str(skin.price)}\n'
        if not index:
            text += '⛔ Скинов нет'
        text += '\n\n' \
                'Введите: <code>Скин смотреть {номер}</code> для предпросмотра\n' \
                'Введите: <code>Скин купить {номер}</code> для покупки скина'

        return await message.reply(text, reply_markup=skin_buy_kb)
    elif len(arg) > 1 and arg[0].lower() in ['предпросмотр', 'посмотреть',
                                              'чекнуть', 'фото', 'скрин',
                                              'смотреть']:
        try:
            index = int(arg[1])
        except:
            return await message.reply('🚫 Неверный номер скина!')

        if index not in skins:
            return await message.reply('🚫 Нет такого скина!')

        skin = skins[index]
        msg = await message.reply_photo(photo=skin.image(),
                                         caption=skin.text,
                                         reply_markup=skin_kb(user.id, index))
        skin.set_image(msg.photo[0].file_id)

    elif len(arg) > 1 and arg[0].lower() in ['покупка', 'купить',
                                              'приобрести', 'поставить']:
        try:
            index = int(arg[1])
        except:
            return await message.reply('🚫 Неверный номер скина!')

        if index not in skins:
            return await message.reply('🚫 Нет такого скина!')

        skin = skins[index]

        if user.balance < skin.price:
            return await message.reply('🚫 Недостаточно денег на руках для покупки!\n'
                                       'Необходимо: {}'.format(to_str(skin.price)))

        user.editmany(balance=user.balance - skin.price, skin=skin.id)

        msg = await message.reply_photo(photo=skin.image(),
                                         caption=skin.text,
                                         reply_markup=skin_kb(user.id, index))
        skin.set_image(msg.photo[0].file_id)
    else:
        skin = skins[user.skin] if user.skin else None
        if skin is None:
            return await message.reply('⛔ У вас нет скина!')
        msg = await message.reply_photo(photo=skin.image(),
                                         caption='🥰 <b>Ваш скин</b>:\n' + skin.text,
                                         reply_markup=skin_kb(user.id, user.skin))
        skin.set_image(msg.photo[0].file_id)


async def skin_call(call: CallbackQuery):
    data = call.data.split('_')
    index = int(data[1])
    user_id = int(data[2])
    if user_id != call.from_user.id:
        return await call.answer('🚫 Это не ваша клавиатура!')
    action = data[3]
    user = User(user=call.from_user)
    skin = skins[index]
    text = f'🥰 <b>Ваш скин</b>:\n{skin.text}' if index == user.skin else skin.text
    img = action if action != "front" else ""
    media = InputMedia(type="photo", media=skin.image(img),
                       caption=text)
    try:
        msg = await call.message.edit_media(media=media,
                                            reply_markup=skin_kb(user.id, user.skin))
        skin.set_image(msg.photo[-1].file_id, img)
    except:
        return
