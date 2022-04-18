import random
import time

from utils.main.cash import to_str
from utils.main.db import sql, timetomin

airplanes = {
    1: {
        'name': 'Мелкая птичка 🛩️',
        'price': 500000,
        'sell_price': 200000,
        'nalog': 10000,
        'limit': 1000000,
        'fuel': 1000
    },
    2: {
        'name': 'Z-25 ✈️',
        'price': 1500000,
        'sell_price': 700000,
        'nalog': 25000,
        'limit': 3000000,
        'fuel': 5000
    },
    3: {
        'name': 'Cilizium ✈️',
        'price': 50000000,
        'sell_price': 25000000,
        'nalog': 2000000,
        'limit': 100000000,
        'fuel': 200000
    },
    4: {
        'name': 'Helixam ✈️',
        'price': 150000000,
        'sell_price': 70000000,
        'nalog': 7000000,
        'limit': 300000000,
        'fuel': 700000
    },
}

all_airplanes_ = [i[1] for i in sql.get_all_data('airplanes')]


def all_airplanes():
    return all_airplanes_


class Airplane:
    def __init__(self, user_id: int):
        self.source: tuple = sql.select_data(user_id, 'owner', True, 'airplanes')
        if self.source is None:
            raise Exception('Not have yaxta')
        self.id: int = self.source[0]
        self.index: int = self.source[1]
        self.airplane = airplanes[self.index]
        self.name: str = self.airplane["name"]
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
        return f'Ваш самолёт: (<b>{self.name}</b>)\n\n' \
               f'💲 Прибыль: {to_str(self.cash)}\n' \
               f'⛽ Состояние: {self.fuel}%\n' \
               f'⚡ Энергия: {self.energy}{xd}\n' \
               f'📠 Налог: {to_str(self.nalog)} / {to_str(self.airplane["limit"])}'

    def edit(self, name, value, attr=True):
        if attr:
            setattr(self, name, value)
        sql.edit_data('id', self.id, name, value, 'airplanes')
        return value

    def editmany(self, attr=True, **kwargs):
        items = kwargs.items()
        query = 'UPDATE airplanes SET '
        items_len = len(items)
        for index, item in enumerate(items):
            if attr:
                setattr(self, item[0], item[1])
            query += f'{item[0]} = {sql.item_to_sql(item[1])}'
            query += ', ' if index < items_len - 1 else ' '
        query += 'WHERE id = {}'.format(self.id)
        sql.execute(query=query, commit=True)

    @staticmethod
    def create(user_id, airplane_index):
        global all_airplanes_
        res = (None, airplane_index, None, 0, None, 0, airplanes[airplane_index]["fuel"], 10, user_id)
        sql.insert_data([res], 'airplanes')
        all_airplanes_.append(res[1])
        return True

    def sell(self):
        sql.delete_data(self.id, 'id', 'airplanes')
        doxod = self.cash + self.airplane['sell_price']
        doxod -= self.nalog
        if doxod < 0:
            doxod = 0
        return doxod

    def ride(self):
        km = random.randint(2, 10)
        doxod = self.airplane['fuel'] * km
        self.editmany(energy=self.energy - 1, cash=self.cash + doxod, fuel=self.fuel - 1,
                      last=time.time())
        return [km, doxod]
