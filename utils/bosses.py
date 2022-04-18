from __future__ import annotations

import random
import time

from utils.items.items import items
from utils.main.cash import to_str
from utils.photos.photos import get_photo, set_photo


actions = ['👊🏿 Вьебали босса с кулачины', '💩 Обосрали босса',
           '🗡️ Выебали босса 1х1 в бравлике', '🤸🏼‍♂️ Ебанули шпагат боссу',
           '🪝 Схватили босса за яйца', '🥲 Пукнули с подливой']


class Boss:
    def __init__(self, name: str, emoji: str, hp: int, img: str, itemsx: list = None):
        if itemsx is None:
            self.items = []
        else:
            self.items = itemsx
        self.time = time.time()
        self.emoji = emoji
        self.name = name + self.emoji
        self.hp = hp
        self.img = 'bosses/' + img
        self.users = {}
        self.len: int = len(self.items) if len(self.items) > 0 else 1

    @property
    def photo(self):
        return get_photo(self.img)

    @photo.setter
    def photo(self, value):
        set_photo(self.img, value)

    @property
    def text(self):
        return '💀 Текущий глобальный босс:\n\n' \
               f'Название: <b>{self.name} {self.emoji}</b>\n' \
               f'Здоровье: <b>{self.hp}</b> ❤️‍🩹\n\n' \
               f'Введите: <code>Босс ударить</code> чтобы ударить босса!'

    async def push(self, user_id: int):
        x = random.randint(1, 5)
        self.hp -= x
        if user_id in self.users:
            self.users[user_id] += 1
        else:
            self.users[user_id] = 1

        choice = random.choice([random.randint(0, self.hp*random.randint(4, 4000)) for _ in range(self.len)] +
                               self.items)
        action = random.choice(actions)

        class Result:
            if type(choice) != str:
                y = to_str(choice)
            else:
                i = items[int(choice)]
                y = f'<b>{i["name"]} {i["emoji"]}</b> <code>(x1)</code>'
            text: str = f'<b>{action}</b> и получили ' \
                        f'{y}\n' \
                        f'💀 Босс: <b>-{x}HP ❤️‍🩹</b>'
            result: int | str = choice

        return Result


bosses = list({
    1: lambda: Boss('Бабиджон', '👶🏼', 100, 'babijon', ['32', '33']),
    2: lambda: Boss('Чмоня', '😼', 150, 'chmonya', ['33', '34']),
    3: lambda: Boss('Мшк Фреде', '🐻', 200, 'freddy', ['35', '33'])
}.values())
boss = None


async def get_global_boss():
    global boss
    if boss and (time.time() - boss.time) < 3600:
        return boss
    boss = random.choice(bosses)()
    return boss
