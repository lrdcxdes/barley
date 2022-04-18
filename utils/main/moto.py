import random
import time

from utils.main.cash import to_str
from utils.main.db import sql, timetomin

motos = {
    1: {
        'name': 'Скутер 🛵',
        'price': 35000,
        'sell_price': 15000,
        'nalog': 2500,
        'limit': 100000,
        'fuel': 500
    },
    2: {
        'name': 'YZF-R1 🏍️',
        'price': 135000,
        'sell_price': 60000,
        'nalog': 5000,
        'limit': 1000000,
        'fuel': 5500
    },
    3: {
        'name': 'Kawasaki 🏍️',
        'price': 535000,
        'sell_price': 250000,
        'nalog': 25000,
        'limit': 2500000,
        'fuel': 30000
    },
    4: {
        'name': 'Suzuki 🏍️',
        'price': 2535000,
        'sell_price': 700000,
        'nalog': 55000,
        'limit': 5500000,
        'fuel': 55000
    },
    5: {
        'name': 'Honda 🏍️',
        'price': 21535000,
        'sell_price': 10000000,
        'nalog': 150000,
        'limit': 55500000,
        'fuel': 250000
    },
    6: {
        'name': 'Ява 🏍️',
        'price': 150000000,
        'sell_price': 70000000,
        'nalog': 2150000,
        'limit': 300000000,
        'fuel': 2250000
    }
}


all_moto_ = [i[1] for i in sql.get_all_data('moto')]


def all_moto():
    return all_moto_


class Moto:
    def __init__(self, user_id: int):
        self.source: tuple = sql.select_data(user_id, 'owner', True, 'moto')
        if self.source is None:
            raise Exception('Not have car')
        self.id: int = self.source[0]
        self.index: int = self.source[1]
        self.moto = motos[self.index]
        self.name: str = self.moto["name"]
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
        return f'Ваша машина: (<b>{self.name}</b>)\n\n' \
               f'💲 Прибыль: {to_str(self.cash)}\n' \
               f'⛽ Состояние: {self.fuel}%\n' \
               f'⚡ Энергия: {self.energy}{xd}\n' \
               f'📠 Налог: {to_str(self.nalog)} / {to_str(self.moto["limit"])}'

    def edit(self, name, value, attr=True):
        if attr:
            setattr(self, name, value)
        sql.edit_data('id', self.id, name, value, 'moto')
        return value

    def editmany(self, attr=True, **kwargs):
        items = kwargs.items()
        query = 'UPDATE moto SET '
        items_len = len(items)
        for index, item in enumerate(items):
            if attr:
                setattr(self, item[0], item[1])
            query += f'{item[0]} = {sql.item_to_sql(item[1])}'
            query += ', ' if index < items_len - 1 else ' '
        query += 'WHERE id = {}'.format(self.id)
        sql.execute(query=query, commit=True)

    @staticmethod
    def create(user_id, moto_index):
        global all_moto_
        res = (None, moto_index, None, 0, None, 0, motos[moto_index]["fuel"], 10, user_id)
        sql.insert_data([res], 'moto')
        all_moto_.append(res[1])
        return True

    def sell(self):
        sql.delete_data(self.id, 'id', 'moto')
        doxod = self.cash + self.moto['sell_price']
        doxod -= self.nalog
        if doxod < 0:
            doxod = 0
        return doxod

    def ride(self):
        km = random.randint(2, 10)
        doxod = self.moto['fuel'] * km
        self.editmany(energy=self.energy - 1, cash=self.cash + doxod, fuel=self.fuel - 1,
                      last=time.time())
        return [km, doxod]
