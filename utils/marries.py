from __future__ import annotations

from datetime import datetime

from utils.main.db import sql


all_marries_ = [i[1] for i in sql.get_all_data('marries')]


def all_marries():
    return all_marries_


class Marry:
    def __init__(self, **kwargs):
        if 'user_id' in kwargs:
            user_id = kwargs['user_id']
            self.source = sql.execute(f'SELECT * FROM marries WHERE user1 = {user_id} OR user2 = {user_id}',
                                      False,
                                      True)
            try:
                self.source = self.source[-1]
            except:
                self.source = None
        elif 'son' in kwargs:
            user_id = kwargs['son']
            self.source = sql.execute(f'SELECT * FROM marries WHERE instr(childs, "{user_id}") > 0 OR instr(zams, '
                                      f'"{user_id}") > 0',
                                      False,
                                      True)
            try:
                self.source = self.source[-1]
            except:
                self.source = None

        if self.source is None:
            raise Exception('NotFoundMarry')

        self.id: int = self.source[0]
        self.user1: int = self.source[1]
        self.user2: int = self.source[2]
        self.reg_date: datetime = datetime.strptime(self.source[3], '%d-%m-%Y %H:%M:%S')
        self.childs: list = [int(i) for i in self.source[4].split(',') if i]
        if len(self.childs) > 100:
            self.childs = self.childs[:100]
        self.balance: int = self.source[5]
        self.last: int | None = self.source[6]
        self.last_sex: int | None = self.source[7]
        self.level: int = self.source[8]
        self.name: str | None = self.source[9]
        self.zams: list = [int(i) for i in self.source[10].split(',') if i]

    def edit(self, name, value, attr=True):
        if attr:
            setattr(self, name, value)
        sql.edit_data('id', self.id, name, value, 'marries')

    def editmany(self, attr=True, **kwargs):
        items = kwargs.items()
        query = 'UPDATE marries SET '
        items_len = len(items)
        for index, item in enumerate(items):
            if attr:
                setattr(self, item[0], item[1])
            query += f'{item[0]} = {sql.item_to_sql(item[1])}'
            query += ', ' if index < items_len - 1 else ' '
        query += 'WHERE id = {}'.format(self.id)
        sql.execute(query=query, commit=True)

    def add_child(self, user_id: int, status='child'):
        if status == 'child':
            if user_id not in self.childs:
                self.childs.append(user_id)
                self.edit('childs', ','.join(str(x) for x in self.childs), False)
            else:
                raise Exception('User in marry!')
        else:
            if user_id not in self.zams:
                self.zams.append(user_id)
                self.edit('zams', ','.join(str(x) for x in self.zams), False)
            else:
                raise Exception('User in marry!')

    @staticmethod
    def create(user1: int, user2: int):
        global all_marries_
        res = (None, user1, user2, datetime.now().strftime('%d-%m-%Y %H:%M:%S'), '', 5000, None, None,
               0, None, '')
        sql.insert_data([res], 'marries')
        all_marries_.append(res[3])
        return res

    def delete(self):
        sql.delete_data(self.id, 'id', 'marries')

    def del_child(self, user_id: int, status='child'):
        if status == 'child':
            self.childs.remove(user_id)
            self.edit('childs', ','.join(str(x) for x in self.childs), False)
        else:
            self.zams.remove(user_id)
            self.edit('zams', ','.join(str(x) for x in self.zams), False)
