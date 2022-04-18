import random
import time

from utils.main.cash import to_str
from utils.main.db import sql, timetomin

rockets = {
    1: {
        'name': 'Пупсик 🚀',
        'price': 350000,
        'sell_price': 150000,
        'nalog': 25000,
        'limit': 1000000,
        'fuel': 3000
    },
    2: {
        'name': 'Обычная ракета 🚀',
        'price': 1350000,
        'sell_price': 600000,
        'nalog': 50000,
        'limit': 3000000,
        'fuel': 16000
    },
    3: {
        'name': 'ZHM-500 🚀',
        'price': 50350000,
        'sell_price': 23500000,
        'nalog': 135000,
        'limit': 100000000,
        'fuel': 105000
    },
}


all_rockets_ = [i[1] for i in sql.get_all_data('rockets')]


def all_rockets():
    return all_rockets_


class Rocket:
    def __init__(self, user_id: int):
        self.source: tuple = sql.select_data(user_id, 'owner', True, 'rockets')
        if self.source is None:
            raise Exception('Not have car')
        self.id: int = self.source[0]
        self.index: int = self.source[1]
        self.rocket = rockets[self.index]
        self.name: str = self.rocket["name"]
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
        return f'Ваша ракета: (<b>{self.name}</b>)\n\n' \
               f'💲 Прибыль: {to_str(self.cash)}\n' \
               f'⛽ Состояние: {self.fuel}%\n' \
               f'⚡ Энергия: {self.energy}{xd}\n' \
               f'📠 Налог: {to_str(self.nalog)} / {to_str(self.rocket["limit"])}'

    def edit(self, name, value, attr=True):
        if attr:
            setattr(self, name, value)
        sql.edit_data('id', self.id, name, value, 'rockets')
        return value

    def editmany(self, attr=True, **kwargs):
        items = kwargs.items()
        query = 'UPDATE rockets SET '
        items_len = len(items)
        for index, item in enumerate(items):
            if attr:
                setattr(self, item[0], item[1])
            query += f'{item[0]} = {sql.item_to_sql(item[1])}'
            query += ', ' if index < items_len - 1 else ' '
        query += 'WHERE id = {}'.format(self.id)
        sql.execute(query=query, commit=True)

    @staticmethod
    def create(user_id, rocket_index):
        global all_rockets_
        res = (None, rocket_index, None, 0, None, 0, rockets[rocket_index]["fuel"], 10, user_id)
        sql.insert_data([res], 'rockets')
        all_rockets_.append(res[1])
        return True

    def sell(self):
        sql.delete_data(self.id, 'id', 'rockets')
        doxod = self.cash + self.rocket['sell_price']
        doxod -= self.nalog
        if doxod < 0:
            doxod = 0
        return doxod

    def ride(self):
        km = random.randint(2, 10)
        doxod = self.rocket['fuel'] * km
        self.editmany(energy=self.energy - 1, cash=self.cash + doxod, fuel=self.fuel - 1,
                      last=time.time())
        return [km, doxod]
