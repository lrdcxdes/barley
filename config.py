"""[[ LK BOT CONFIG ]]"""

"""Import aiofile для курсов валют"""
from aiofile import async_open


""" Основные настройки """
token = "123:AAFKg123pkJsSpE"  # Bot Token @BotFather
owner_id = 2072301163  # Айди владельца бота
database = "assets/database"  # Путь к базе данных
bot_name = "barleygamebot"  # Никнейм бота

log = True  # Включить логирование
bonus = 50000  # Ежедневный бонус для игроков
zarefa = 15000  # За 1 реферала дают денег
credit_limit = 50000  # Кредитный лимит
credit_percent = 0  # Забей


""" Донат бота """
coins_obmen_enabled = False

payok = False  # Payok.io платежка включена?
payok_api_id = 312  # Payok.io API ID
payok_shop_id = 1142  # Payok.io магазин ID
payok_secret = "f43f5a50691237c3d"  # Payok.io Секретный ключ
payok_api_key = "2-11D3E3111209-3"
# Payok.io Api key

freekassa = False  # freekassa.ru включена?
freekassa_shop_id = 12902  # freekassa.ru магазин ID
freekassa_secrets = [
    "Bl124",  # freekassa.ru Секретный ключ 1
    "_d912312*Yv{C8-",  # freekassa.ru Секретный ключ 2
]
freekassa_api_key = "8815e14904123d509ff76b7"  # freekassa.ru Api key


donates = {
    1: {"name": "💎 VIP", "price": 150, "percent": 1, "cash": 100000, "prefix": "💎"},
    2: {
        "name": "🥋 JUNIOR",
        "price": 1000,
        "percent": 2,
        "cash": 1000000,
        "prefix": "🥋",
    },
    3: {
        "name": "❤️‍🔥 ADMIN",
        "price": 5000,
        "percent": 3,
        "cash": 10000000,
        "prefix": "❤️‍🔥",
    },
    4: {
        "name": "🧑🏼‍💻 Кодер",
        "price": 10000000,
        "percent": 10,
        "cash": 1000000000,
        "prefix": "🧑🏼‍💻",
    },
    5: {
        "name": "👻 Уник",
        "prefix": "👻",
        "price": 10000,
        "percent": 5,
        "cash": 100000000,
    },
}


""" Курсы валют """
bitcoin_price_ = float(open("assets/btc.price", "r", encoding="utf-8").read())


def bitcoin_price():
    return bitcoin_price_


async def set_bitcoin_price(value: int):
    global bitcoin_price_
    if value <= 0:
        value = 1
    bitcoin_price_ = value
    async with async_open("assets/btc.price", "w") as file:
        await file.write(str(value))


euro_price_ = float(open("assets/euro.price", "r", encoding="utf-8").read())


def euro_price():
    return euro_price_


async def set_euro_price(value: int):
    global euro_price_
    if value <= 0:
        value = 1
    euro_price_ = value
    async with async_open("assets/euro.price", "w") as file:
        await file.write(str(value))


uah_price_ = float(open("assets/uah.price", "r", encoding="utf-8").read())


def uah_price():
    return uah_price_


async def set_uah_price(value: int):
    global uah_price_
    if value <= 0:
        value = 1
    uah_price_ = value
    async with async_open("assets/uah.price", "w") as file:
        await file.write(str(value))
