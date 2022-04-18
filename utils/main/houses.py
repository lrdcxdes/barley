import time

from utils.main.cash import to_str
from utils.main.db import sql, timetomin

houses = {
    1: {
        'name': 'Коробочка 📦',
        'price': 15000,
        'sell_price': 7500,
        'doxod': 250,
        'nalog': 150,
        'limit': 50000
    },
    2: {
        'name': 'Сарай 🛖',
        'price': 50000,
        'sell_price': 20000,
        'doxod': 1000,
        'nalog': 450,
        'limit': 75000
    },
    3: {
        'name': 'Обычный дом 🏠',
        'price': 125000,
        'sell_price': 50000,
        'doxod': 5100,
        'nalog': 2450,
        'limit': 100000
    },
    4: {
        'name': 'Вилла 🏫',
        'price': 750000,
        'sell_price': 455000,
        'doxod': 15500,
        'nalog': 7500,
        'limit': 300000
    },
    5: {
        'name': 'Пентхаус 🏯',
        'price': 1525000,
        'sell_price': 700500,
        'doxod': 55000,
        'nalog': 27500,
        'limit': 500000
    },
    6: {
        'name': 'Stark Tower 👨‍🎤',
        'price': 10500000,
        'sell_price': 4500000,
        'doxod': 125000,
        'nalog': 65000,
        'limit': 5000000
    }
}


all_houses_ = [i[1] for i in sql.get_all_data('houses')]


def all_houses():
    return all_houses_


class House:
    def __init__(self, user_id: int):
        self.source: tuple = sql.select_data(user_id, 'owner', True, 'houses')
        if self.source is None:
            raise Exception('Not have house')
        self.id: int = self.source[0]
        self.index: int = self.source[1]
        self.house = houses[self.index]
        self.name: str = self.source[2] if self.source[2] else self.house['name']
        self.cash: int = self.source[3]
        self.last: int = self.source[4]
        self.nalog: int = self.source[5]
        self.arenda = bool(self.source[6])
        self.owner: int = self.source[7]

    @property
    def text(self):
        xd = f' ({timetomin(int(time.time() - self.last))})' if self.last is not None else ''
        return f'🏠 Ваш дом (<b>{self.name}</b>)\n\n' \
               f'💲 Прибыль: {to_str(self.cash)}{xd}\n' \
               f'🅰️ В аренде: {"Да ✅" if self.arenda else "Нет ❌"}\n' \
               f'📠 Налог: {to_str(self.nalog)} / {to_str(houses[self.index]["limit"])}'

    def edit(self, name, value, attr=True):
        if attr:
            setattr(self, name, value)
        sql.edit_data('id', self.id, name, value, 'houses')
        return value

    def editmany(self, attr=True, **kwargs):
        items = kwargs.items()
        query = 'UPDATE houses SET '
        items_len = len(items)
        for index, item in enumerate(items):
            if attr:
                setattr(self, item[0], item[1])
            query += f'{item[0]} = {sql.item_to_sql(item[1])}'
            query += ', ' if index < items_len - 1 else ' '
        query += 'WHERE id = {}'.format(self.id)
        sql.execute(query=query, commit=True)

    @staticmethod
    def create(user_id, house_index):
        global all_houses_
        res = (None, house_index, None, 0, None, 0, False, user_id)
        sql.insert_data([res], 'houses')
        all_houses_.append(res[1])
        return True

    def sell(self):
        sql.delete_data(self.id, 'id', 'houses')
        doxod = self.cash + self.house['sell_price']
        doxod -= self.nalog
        if doxod < 0:
            doxod = 0
        return doxod
