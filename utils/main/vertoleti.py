import random
import time

from utils.main.cash import to_str
from utils.main.db import sql, timetomin

vertoleti = {
    1: {
        'name': 'Striker 🚁',
        'price': 12500000,
        'sell_price': 6000000,
        'nalog': 300000,
        'limit': 30000000,
        'fuel': 250000
    },
    2: {
        'name': 'Elyster 🚁',
        'price': 50000000,
        'sell_price': 20000000,
        'nalog': 1000000,
        'limit': 100000000,
        'fuel': 1000000
    },
    3: {
        'name': 'Penisax 🚁',
        'price': 150000000,
        'sell_price': 60000000,
        'nalog': 12500000,
        'limit': 250000000,
        'fuel': 1200000
    },
    4: {
        'name': 'Kaliformn 🚁',
        'price': 12000000000,
        'sell_price': 55000000,
        'nalog': 25000000,
        'limit': 250000000,
        'fuel': 3000000
    },
}


all_vertoleti_ = [i[1] for i in sql.get_all_data('vertoleti')]


def all_vertoleti():
    return all_vertoleti_


class Vertolet:
    def __init__(self, user_id: int):
        self.source: tuple = sql.select_data(user_id, 'owner', True, 'vertoleti')
        if self.source is None:
            raise Exception('Not have vertolet')
        self.id: int = self.source[0]
        self.index: int = self.source[1]
        self.vertolet = vertoleti[self.index]
        self.name: str = self.vertolet["name"]
        self.number: str = self.source[2]
        self.cash: int = self.source[3]
        self.last: int = self.source[4]
        self.nalog: int = self.source[5]
        self.fuel: int = self.source[6]
        self.energy: int = self.source[7]
        self.owner: int = self.source[8]

    @property
    def text(self):
        xd = f' ({timetomin(int(time.time() - self.last))})' if self.last is not None else ''
        return f'Ваш вертолёт: (<b>{self.name}</b>)\n\n' \
               f'💲 Прибыль: {to_str(self.cash)}\n' \
               f'⛽ Состояние: {self.fuel}%\n' \
               f'⚡ Энергия: {self.energy}{xd}\n' \
               f'📠 Налог: {to_str(self.nalog)} / {to_str(self.vertolet["limit"])}'

    def edit(self, name, value, attr=True):
        if attr:
            setattr(self, name, value)
        sql.edit_data('id', self.id, name, value, 'vertoleti')
        return value

    def editmany(self, attr=True, **kwargs):
        items = kwargs.items()
        query = 'UPDATE vertoleti SET '
        items_len = len(items)
        for index, item in enumerate(items):
            if attr:
                setattr(self, item[0], item[1])
            query += f'{item[0]} = {sql.item_to_sql(item[1])}'
            query += ', ' if index < items_len - 1 else ' '
        query += 'WHERE id = {}'.format(self.id)
        sql.execute(query=query, commit=True)

    @staticmethod
    def create(user_id, vertolet_index):
        global all_vertoleti_
        res = (None, vertolet_index, None, 0, None, 0, vertoleti[vertolet_index]["fuel"], 10, user_id)
        sql.insert_data([res], 'vertoleti')
        all_vertoleti_.append(vertolet_index)
        return True

    def sell(self):
        sql.delete_data(self.id, 'id', 'vertoleti')
        doxod = self.cash + self.vertolet['sell_price']
        doxod -= self.nalog
        if doxod < 0:
            doxod = 0
        return doxod

    def ride(self):
        km = random.randint(2, 10)
        doxod = self.vertolet['fuel'] * km
        self.editmany(energy=self.energy - 1, cash=self.cash + doxod, fuel=self.fuel - 1,
                      last=time.time())
        return [km, doxod]
