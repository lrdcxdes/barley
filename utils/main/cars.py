import random
import time

from utils.main.cash import to_str
from utils.main.db import sql, timetomin

cars = {
    1: {
        'name': 'Жигули 🚗',
        'price': 50000,
        'sell_price': 20000,
        'nalog': 2500,
        'limit': 100000,
        'fuel': 500
    },
    2: {
        'name': 'Audi 🚗',
        'price': 250000,
        'sell_price': 115000,
        'nalog': 10000,
        'limit': 500000,
        'fuel': 5000
        },
    3: {
        'name': 'BMW 🚗',
        'price': 1000000,
        'sell_price': 450000,
        'nalog': 50000,
        'limit': 2000000,
        'fuel': 10000
        },
    4: {
        'name': 'Bentley 🚗',
        'price': 5000000,
        'sell_price': 2250000,
        'nalog': 100000,
        'limit': 10000000,
        'fuel': 50000
        },
    5: {
        'name': 'Formula 1 🏎️',
        'price': 25000000,
        'sell_price': 12000000,
        'nalog': 250000,
        'limit': 50000000,
        'fuel': 100000
    },
    6: {
        'name': 'Tesla Roadster 🛰️',
        'price': 50000000,
        'sell_price': 23500000,
        'nalog': 1000000,
        'limit': 1000000000,
        'fuel': 150000
    }
}


all_cars_ = [i[1] for i in sql.get_all_data('cars')]


def all_cars():
    return all_cars_


class Car:
    def __init__(self, user_id: int):
        self.source: tuple = sql.select_data(user_id, 'owner', True, 'cars')
        if self.source is None:
            raise Exception('Not have car')
        self.id: int = self.source[0]
        self.index: int = self.source[1]
        self.car = cars[self.index]
        self.name: str = self.car["name"]
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
               f'📠 Налог: {to_str(self.nalog)} / {to_str(self.car["limit"])}'

    def edit(self, name, value, attr=True):
        if attr:
            setattr(self, name, value)
        sql.edit_data('id', self.id, name, value, 'cars')
        return value

    def editmany(self, attr=True, **kwargs):
        items = kwargs.items()
        query = 'UPDATE cars SET '
        items_len = len(items)
        for index, item in enumerate(items):
            if attr:
                setattr(self, item[0], item[1])
            query += f'{item[0]} = {sql.item_to_sql(item[1])}'
            query += ', ' if index < items_len - 1 else ' '
        query += 'WHERE id = {}'.format(self.id)
        sql.execute(query=query, commit=True)

    @staticmethod
    def create(user_id, car_index):
        global all_cars_
        res = (None, car_index, None, 0, None, 0, cars[car_index]["fuel"], 10, user_id)
        sql.insert_data([res], 'cars')
        all_cars_.append(res[1])
        return True

    def sell(self):
        sql.delete_data(self.id, 'id', 'cars')
        doxod = self.cash + self.car['sell_price']
        doxod -= self.nalog
        if doxod < 0:
            doxod = 0
        return doxod

    def ride(self):
        km = random.randint(2, 10)
        doxod = self.car['fuel'] * km
        self.editmany(energy=self.energy - 1, cash=self.cash + doxod, fuel=self.fuel - 1,
                      last=time.time())
        return [km, doxod]
