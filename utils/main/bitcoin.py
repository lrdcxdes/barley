import time

import config
from utils.main.cash import to_str
from utils.main.db import sql, timetomin


class Ferma:
    def __init__(self, name: str, price: int, doxod: float, nalog: int, limit: int, limit_video: int):
        self.name = name
        self.price = price
        self.doxod = doxod
        self.nalog = nalog
        self.limit = limit
        self.videoprice = price // 3.5
        self.limit_video = limit_video


bitcoins = {
    1: lambda: Ferma('Мини-Ферма 💻', 150000, 1.5, 17500, 300000, 1000),
    2: lambda: Ferma('Экзо-Ферма 🧑🏿‍💻', 2500000, 5.1, 150000, 5000000, 2000),
    3: lambda: Ferma('Мега-ферма 🖥️', 15000000, 50, 5000000, 100000000, 3000),
    4: lambda: Ferma('Авто-ферма 📼', 1000000000, 1000, 10000000, 2000000000, 4000)
}


to_usd = lambda summ: int(float(summ) * config.bitcoin_price())


class Bitcoin:
    @staticmethod
    def create(owner: int, zindex: int):
        res = (None, owner, zindex, 0, time.time(), 0.0, 0)
        sql.insert_data([res], 'bitcoin')
        return res

    def __init__(self, owner: int = None):
        self.source = sql.select_data(owner, 'owner', True, 'bitcoin')

        self.id: int = self.source[0]
        self.owner: int = self.source[1]
        self.zindex: int = self.source[2]
        self.balance_: float = round(self.source[3], 8)
        self.last: int = self.source[4]
        self.videocards: int = self.source[5]
        self.nalog: int = self.source[6]
        self.bitcoin: Ferma = bitcoins[self.zindex]()
        self.bitcoin.doxod *= self.videocards

    def edit(self, name, value, attr=True):
        if attr:
            setattr(self, name, value)
        sql.edit_data('id', self.id, name, value, 'bitcoin')
        return value

    def editmany(self, attr=True, **kwargs):
        items = kwargs.items()
        query = 'UPDATE bitcoin SET '
        items_len = len(items)
        for index, item in enumerate(items):
            if attr:
                setattr(self, item[0], item[1])
            query += f'{item[0]} = {sql.item_to_sql(item[1])}'
            query += ', ' if index < items_len - 1 else ' '
        query += 'WHERE id = {}'.format(self.id)
        sql.execute(query=query, commit=True)

    def sell(self):
        sql.delete_data(self.id, 'id', 'bitcoin')
        doxod = to_usd(self.balance_) + self.bitcoin.price // 2.1
        doxod += self.bitcoin.videoprice * self.videocards
        doxod -= self.nalog
        if doxod < 0:
            doxod = 0
        return doxod

    @property
    def text(self):
        return f'🖥️ Ваша биткоин ферма:\n' \
               f'➖➖➖➖➖➖➖➖➖➖➖\n' \
               f'🖥️ Название: <b>{self.bitcoin.name}</b>\n' \
               f'🧀 Баланс: <b>{int(self.balance)}</b> (~{to_str(to_usd(int(self.balance_)))} USD)\n' \
               f'🌫️ Вы вложили: {to_str(int(self.videocards * (self.bitcoin.price // 4)))}\n' \
               f'➖➖➖➖➖➖➖➖➖➖➖\n' \
               f'📼 Кол-во видеокарт: <b>{self.videocards} / {self.bitcoin.limit_video}</b>\n' \
               f'💸 Доход: <b>{self.bitcoin.doxod}</b>BTC/час (~{to_str(to_usd(self.bitcoin.doxod))} USD)\n' \
               f'⌛ След. через: <code>{timetomin(int(time.time() - self.last))}</code>\n' \
               f'💲 Налог: <code>{to_str(self.nalog)} / {to_str(self.bitcoin.limit)}</code>'

    @property
    def balance(self):
        return self.balance_

    @balance.setter
    def balance(self, value):
        self.balance_ = value
