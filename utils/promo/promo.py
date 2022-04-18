from __future__ import annotations
from utils.main.db import sql


all_promo_ = [str(i[1]).lower() for i in sql.get_all_data('promocodes')]


def all_promo():
    return all_promo_


class Promocode:
    def __init__(self, name: str):
        self.source = sql.execute(f'SELECT * FROM promocodes WHERE LOWER(name) = "{name}"', False, True)
        if len(self.source) == 0:
            raise Exception('Промокод не найден!')
        self.source = self.source[-1]

        self.id: int = self.source[0]
        self.name: str = str(self.source[1])
        self.activations: int = self.source[2]
        self.users: list = [int(x) for x in self.source[3].split(',') if x]
        self.status: bool = bool(self.source[4])
        self.summ: int = self.source[5]
        self.xd: int = self.source[6]

    def add_user(self, user_id: int):
        self.users.append(user_id)
        sql.edit_data('id', self.id, 'users', ','.join(str(x) for x in self.users), 'promocodes')

    def finish(self):
        sql.edit_data('id', self.id, 'status', False, 'promocodes')

    @staticmethod
    def create(name: str, activations: int, summ: int, xd: int):
        global all_promo_
        res = (None, name.lower(), activations, '', True, summ, xd)
        sql.insert_data([res], 'promocodes')
        all_promo_.append(name)
