import time

items = {
    -1: {
        "name": "Деньги",
        "emoji": "💸",
        "sell_price": 1
    },
    1: {
        "name": "Корм",
        "emoji": "🥜",
        "sell_price": 1500,
        'use': 'energy'
    },
    2: {
        "name": "Обычный кейс",
        "emoji": "🥡",
        "sell_price": 15000000
    },
    3: {
        "name": "Средний кейс",
        "emoji": "🎁",
        "sell_price": 50000000
    },
    4: {
        "name": "Ультра кейс",
        "sell_price": 1000000000,
        "emoji": "☄️"
    },
    5: {
        "name": 'Очки',
        "emoji": "🕶️",
        "sell_price": 2500,
        'use': 'xp'
    },
    6: {
        "name": 'Кости',
        "emoji": '🦴',
        'sell_price': 1000,
        'use': 'xp'
    },
    7: {
        "name": "Конфетка",
        "emoji": '🍭',
        'sell_price': 9000,
        'use': 'energy'
    },
    8: {
        "name": 'Зуб',
        'emoji': '🦷',
        'sell_price': 4500,
        'use': 'xp'
    },
    9: {
        "name": 'Билет в автосалон',
        'emoji': '🎟️',
        'sell_price': 500000,
        'use': 'sell_count'
    },
    10: {
        "name": "Мячик",
        "emoji": '⚾',
        "sell_price": 5500,
        'use': 'energy'
    },
    11: {
        "name": "Бриллиант",
        "emoji": "💎",
        "sell_price": 150000,
        'use': 'sell_count'
    },
    12: {
        "name": "Ключ от дома",
        'emoji': '🔑',
        "sell_price": 1500000,
        'use': 'sell_count'
    },
    13: {
        "name": 'Волшебная палочка',
        'emoji': '🪄',
        'sell_price': 30000,
        'use': 'sell_count'
    },
    14: {
        "name": "Мона Лиза",
        "emoji": "🖼️",
        "sell_price": 5600000,
        'use': 'sell_count'
    },
    15: {
        'name': 'Камень',
        'emoji': '🪨',
        'sell_price': 15,
        'xp': 0
    },
    16: {
        "name": 'Медь',
        'emoji': '🌰',
        'sell_price': 35,
        'xp': 50,
    },
    17: {
        'name': 'Серебро',
        'emoji': '🪙',
        'sell_price': 55,
        'xp': 150
    },
    18: {
        'name': 'Золото',
        'emoji': '🌼',
        'sell_price': 100,
        'xp': 500
    },
    19: {
        'name': 'Хрусталь',
        'emoji': '🧊',
        'sell_price': 250,
        'xp': 1000
    },
    20: {
        'name': 'Плазма',
        'emoji': '🌫',
        'sell_price': 1000,
        'xp': 5000
    },
    21: {
        "name": "Шестерёнка",
        'emoji': '⚙️',
        'sell_price': 15,
        'xp': 0
    },
    22: {
        'name': 'Болтик',
        'emoji': '🔩',
        'sell_price': 35,
        'xp': 50
    },
    23: {
        'name': 'Гаечка',
        'emoji': '🔧',
        'sell_price': 100,
        'xp': 500
    },
    24: {
        'name': 'Гвоздь',
        'emoji': '🔨',
        'sell_price': 250,
        'xp': 1000
    },
    25: {
        'name': 'Отвёртка',
        'emoji': '🪛',
        'sell_price': 1000,
        'xp': 5000
    },
    26: {
        'name': 'Звёздочка',
        'emoji': '⭐',
        'sell_price': 166000,
    },
    27: {
        'name': 'Пэпси',
        'emoji': '🥤',
        'sell_price': 100,
        'xp': 0
    },
    28: {
        'name': 'Кока-Льока',
        'emoji': '🍹',
        'sell_price': 2500,
        'xp': 100
    },
    29: {
        'name': 'Трахун',
        'emoji': '🍸',
        'sell_price': 15000,
        'xp': 300
    },
    30: {
        'name': 'Квас',
        'emoji': '🍺',
        'sell_price': 25000,
        'xp': 500
    },
    31: {
        'name': 'Крабовый Салат',
        'emoji': '🥗',
        'sell_price': 5000,
        'use': 'energy'
    },
    32: {
        'name': 'Милкшейк',
        'emoji': '🍼',
        'sell_price': 9100,
        'use': 'energy'
    },
    33: {
        'name': 'Какашечка',
        'emoji': '💩',
        'sell_price': 1
    },
    34: {
        'name': 'Деловой Костюм',
        'emoji': '👔',
        'sell_price': 15000,
        'use': 'xp'
    },
    35: {
        'name': 'Маска',
        'emoji': '🎭',
        'sell_price': 20000,
        'use': 'xp'
    },
}


async def use_item(user, item: dict, count: int):
    a1 = lambda: user.edit('energy', user.energy + count)
    a2 = lambda: user.edit('xp', user.xp + count)
    a3 = lambda: user.editmany(sell_count=user.sell_count + count if user.sell_count
                                                                     is not None else count)
    actions = {
        'energy': [a1, f'<b>+⚡ {count} Энергии</b>'],
        'xp': [a2, f'<b>+♟️ {count} XP</b>'],
        'sell_count': [a3, f'<b>+🎫 {count} Скидка на покупки</b>']
    }
    xd = actions[item['use']]
    xd[0]()
    return xd[1]
