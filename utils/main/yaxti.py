import random
import time

from utils.main.cash import to_str
from utils.main.db import sql, timetomin

yaxti = {
    1: {
        'name': 'Маленькая яхта ⛵',
        'price': 150000,
        'sell_price': 20000,
        'nalog': 500,
        'limit': 100000,
        'fuel': 1000
    },
    2: {
        'name': 'Большая яхта ⛵',
        'price': 1000000,
        'sell_price': 450000,
        'nalog': 10000,
        'limit': 2500000,
        'fuel': 15000
    },
    3: {
        'name': 'Средняя яхта ⛵',
        'price': 3500000,
        'sell_price': 1700000,
        'nalog': 15000,
        'limit': 7000000,
        'fuel': 30000
    },
    4: {
        'name': 'Яхта Тони Старка 🚢',
        'price': 15000000,
        'sell_price': 7000000,
        'nalog': 150000,
        'limit': 30000000,
        'fuel': 100000
    }
}


all_yaxti_ = [i[1] for i in sql.get_all_data('yaxti')]


def all_yaxti():
    return all_yaxti_


class Yaxta:
    def __init__(self, user_id: int):
        self.source: tuple = sql.select_data(user_id, 'owner', True, 'yaxti')
        if self.source is None:
            raise Exception('Not have yaxta')
        self.id: int = self.source[0]
        self.index: int = self.source[1]
        self.yaxta = yaxti[self.index]
        self.name: str = self.yaxta["name"]
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
        return f'Ваша яхта: (<b>{self.name}</b>)\n\n' \
               f'💲 Прибыль: {to_str(self.cash)}\n' \
               f'⛽ Состояние: {self.fuel}%\n' \
               f'⚡ Энергия: {self.energy}{xd}\n' \
               f'📠 Налог: {to_str(self.nalog)} / {to_str(self.yaxta["limit"])}'

    def edit(self, name, value, attr=True):
        if attr:
            setattr(self, name, value)
        sql.edit_data('id', self.id, name, value, 'yaxti')
        return value

    def editmany(self, attr=True, **kwargs):
        items = kwargs.items()
        query = 'UPDATE yaxti SET '
        items_len = len(items)
        for index, item in enumerate(items):
            if attr:
                setattr(self, item[0], item[1])
            query += f'{item[0]} = {sql.item_to_sql(item[1])}'
            query += ', ' if index < items_len - 1 else ' '
        query += 'WHERE id = {}'.format(self.id)
        sql.execute(query=query, commit=True)

    @staticmethod
    def create(user_id, yaxta_index):
        global all_yaxti_
        res = (None, yaxta_index, None, 0, None, 0, yaxti[yaxta_index]["fuel"], 10, user_id)
        sql.insert_data([res], 'yaxti')
        all_yaxti_.append(yaxta_index)
        return True

    def sell(self):
        sql.delete_data(self.id, 'id', 'yaxti')
        doxod = self.cash + self.yaxta['sell_price']
        doxod -= self.nalog
        if doxod < 0:
            doxod = 0
        return doxod

    def ride(self):
        km = random.randint(2, 10)
        doxod = self.yaxta['fuel'] * km
        self.editmany(energy=self.energy - 1, cash=self.cash + doxod, fuel=self.fuel - 1,
                      last=time.time())
        return [km, doxod]
