from aiogram.types import Message, CallbackQuery
from handlers.users.donate import zadonatit_handler
from keyboard.help import help_kb, back_kb
from keyboard.main import invite_kb
from utils.main.chats import Chat
from utils.main.users import User


async def start_handler(message: Message):
    if message.chat.id != message.from_user.id:
        Chat(chat=message.chat)
    else:
        User(user=message.from_user)
        if message.get_args().lower() == 'задонатить':
            return await zadonatit_handler(message)
    text = '<a href="https://t.me/barleygamebot">🍻</a> Игровой бот <b>Barley BOT</b> приветствует тебя!\n' \
           '😇 Помощь: /help (все доступные команды)\n' \
           '🅰️ Админ: <a href="https://t.me/lord_code">@admin</a>\n' \
           '💒 Игровой чат: @barleychat\n' \
           '🗞️ Новости и промокоды: @barleygame\n' \
           '➖➖➖➖➖➖➖➖➖➖➖➖➖\n' \
           '📉 Уникальные системы, игры, экономика'
    return await message.answer(text=text, reply_markup=invite_kb)


async def help_handler(message: Message):
    return await message.reply(text=actions_help['back'], reply_markup=help_kb)


actions_help = {
    'back': '''<a href="https://t.me/barleygamebot">👻</a> Документация: https://teletype.in/@lordcodes/barley
🗞️ Промокоды и новости: @barleygame
💟 Игровой чат: @barleychat
🅰️ По всем вопросам: <a href="https://t.me/lord_code">@admin</a>
➖➖➖➖➖➖➖➖➖➖➖➖➖
<b>👇🏿 Выберите категорию 👇🏿</b>''',

    'main': '''<b>🆘 Помощь</b> - Открыть это меню
<b>💰 Баланс (Б)</b> - Посмотреть баланс
<b>👤 Профиль (П)</b> - Посмотреть профиль
<b>😎 Ник</b> *{ник} - Установить никнейм
<b>🔔 Уведы</b> - ВКЛ/ВЫКЛ упоминания
<b>🔝 Топ</b> - Топ пользователей
<b>🏦 Банк</b> - Операции с банком
<b>💳 Деп</b> - Операции с депозитом
<b>💸 Кредит</b> - Операции с кредитом
<b>🐶 Пет</b> - Питомцы
<b>🎒 Инв</b> - Инвентарь
<b>🧕🏼 Скин</b> - Скины
<b>🤝🏿 Дать</b> - Передать деньги
<b>🎁 Бонус</b> - Ежедневный бонус
<b>🎁 Промо</b> - Активировать промокод
<b>🎁 Промо создать</b> - Создать промокод
<b>👥 Реф</b> - Реф. система''',

    'games': '''<b>🎲 Кубик</b> - Подкинуть кубик
<b>🎰 Казино</b> - Крутить слоты
<b>🍒 Рулетка</b> - Играть в рулетку
<b>📉 Нвути</b> - Играть в Больше-Меньше
<b>🪙 Флип</b> - Орёл или Решка
<b>🎳 Боулинг</b> - Играть в боулинг
<b>🎯 Дартс</b> - Играть в дартс
<b>🪨 КНБ</b> - Играть в Цу-е-фа
<b>📦 Кейсы</b> - Открывать кейсы''',

    'work': '''<b>⛏️ Шахта</b> - Система шахты
<b>🏭 Завод</b> - Система завода
<b>🍾 Бутылки</b> - Система бутылок
➖➖➖➖➖➖➖➖➖➖➖➖➖
<b>💪🏿 Работа</b> - Профессия и жизнь
<b>🧛🏿 Ограбить</b> - Система воровства''',

    'imush': '''<b>🏠 Дом</b> - Система домов
<b>🧑🏿‍💼 Биз</b> - Система бизнесов
<b>🏎️ Машина</b> - Система машин
<b>🚁 Вертолёт</b> - Система вертолётов
<b>✈️ Самолёт</b> - Система самолётов
<b>🏍️ Мото</b> - Система мотоцикл
<b>🪖 Танк</b> - Система танков
<b>⛵ Яхта</b> - Система яхт
<b>🚀 Ракета</b> - Система ракет
<b>💲 Налог</b> - Общий налог на всё''',

    'unik': '''<b>👨‍👩‍👦 Брак</b> - Система семьи
<b>⭐ Биткоин</b> - Система BTC и Ферм
<b>🇮🇨 Страны</b> - Система государств
<b>😇 Префикс</b> - Система префиксов
<b>🈹 Скины</b> - Система скинов
<b>💶 Евро</b> - Система евро
<b>💷 Гривны</b> - Система гривен
<b>👻 Босс<b> - Система боссов
<b>🏪 Шоп</b> - Магазин''',

    'other': '''<b>📃 Ласт</b> - Недавние действия
<b>🪙 Донат</b> - Система доната и привилегий
<b>📈 Курс</b> - Курс биткоина
<b>🛡️ Щит</b> - Щиты от воровства
<b>🔇 Мут</b> - Замутить пользователя
<b>💥 Бан</b> - Забанить пользователя
<b>🔈 Анмут</b> - Размутить пользователя
<b>😁 Разбан</b> - Разбанить пользователя
<b>🪙 Кобмен</b> - Обменять коины на доллары
<b>💲 Обмен</b> - Обменять доллары на коины
<b>👌🏿 Процент</b> - Купить доп. процент к депозиту
<b>😇 РП</b> - РП Действия'''
}


async def help_call_handler(call: CallbackQuery):
    action = call.data.split('_')[1]
    text = actions_help[action]
    try:
        return await call.message.edit_text(text=text, reply_markup=back_kb if action != 'back' else help_kb)
    except:
        return await call.answer('😎')
