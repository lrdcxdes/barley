from __future__ import annotations

import re
from datetime import datetime
from threading import Thread
import time

from aiogram import Bot

import config
from utils.jobs.jobs import Job, levels
from utils.main.cash import to_str
from utils.main.db import sql, timetomin
from utils.main.donates import Donate

all_users_ = [i[0] for i in sql.get_all_data()]


def all_users():
    return all_users_
    
    
datetime_bonus = datetime(year=1920, month=1, day=1).strftime('%d-%m-%Y %H:%M:%S')


class User:
    @staticmethod
    def create(user_id: int, first_name: str = None, username: str = None, ref_id: int = None):
        global all_users_
        now_date = datetime.now()
        reg_date = now_date.strftime('%d-%m-%Y %H:%M:%S')
        res = (user_id, None, username, first_name, reg_date, False, 5000, 0, 0, '', '', None,
               datetime_bonus, ref_id, 0, False, 0, None, 10, None,
               0, 0, 0, 0, None, None, 0, 0, None, None, None, 0.0, 0, False, 0, False)
        sql.insert_data([res])
        all_users_.append(res[0])
        return res

    def __init__(self, **kwargs):
        first_name = None
        username = None
        uid = None

        if 'user' in kwargs:
            user = kwargs['user']
            uid = user.id
            first_name = re.sub(r'[^a-zA-Zа-яА-Я0-9]', '', user.first_name)
            if len(first_name) < 4:
                first_name = first_name + 'A' * (4 - len(first_name))
            elif len(first_name) > 16:
                first_name = first_name[:16]
            username = user.username
            self.source: tuple = sql.select_data(name=uid, title='id',
                                                 row_factor=True)
        elif 'id' in kwargs:
            uid = kwargs['id']
            self.source: tuple = sql.select_data(name=uid, title='id',
                                                 row_factor=True)
        elif 'username' in kwargs:
            username = kwargs['username'].lower()
            try:
                self.source: tuple = sql.execute(query=f'SELECT * FROM users WHERE username IS NOT NULL AND LOWER('
                                                       f'username) = "{username}"',
                                                 fetch=True)[0]
            except Exception as ex:
                print(ex)
                self.source = None
        else:
            x = next(iter(kwargs.items()))
            self.source: tuple = sql.select_data(name=x[1], title=x[0],
                                                 row_factor=True)

        if self.source is None and (uid is None or 'check_ref' in kwargs):
            raise Exception('UserNotFound')
        elif self.source is None:
            self.source = User.create(uid, first_name, username)

        self.id: int = self.source[0]
        self.name: str | None = self.source[1]
        self.username: str = self.source[2]
        self.first_name: str | None = self.source[3]
        self.reg_date: datetime = datetime.strptime(self.source[4], '%d-%m-%Y %H:%M:%S')
        self.notifies = bool(self.source[5])
        self.balance: int = self.source[6]
        self.bank: int = self.source[7]
        self.deposit: int = self.source[8]
        self.pets: iter = (int(x) for x in self.source[9].split(',') if x)
        self.items: iter | list = ([int(x.split(':')[0]), int(x.split(':')[1])] for x in self.source[10].split(','
                                                                                                               ) if x
        and ':' in x)
        self.deposit_date: int | None = self.source[11]
        self.bonus: datetime = datetime.strptime(self.source[12], '%d-%m-%Y %H:%M:%S')
        self.ref: int | None = self.source[13]
        self.refs: int = self.source[14]
        self.lock: bool = bool(self.source[15])

        self.credit: int = self.source[16]
        self.credit_time: int | None = self.source[17]

        self.energy: int = self.source[18]
        self.energy_time: int | None = self.source[19]

        self.xp: int = self.source[20]
        self.sell_count: int = self.source[21]

        self.level: int = self.source[22]
        self.level_json: dict = levels.get(self.level) if levels.get(self.level) else levels[12]
        self.job_index: int = self.source[23]
        self.job = Job(index=self.job_index) if self.job_index > 0 else None
        self.job_time: int | None = self.source[24]
        self.work_time: int | None = self.source[25]

        self.percent: int = self.source[26]
        self.coins: int = self.source[27]
        self.donate_source: str = self.source[28]

        self.prefix: str | None = self.source[29]

        self.admin_last: datetime | None = datetime.strptime(self.source[30], '%d-%m-%Y %H:%M:%S') if self.source[30] \
            else None

        self.last_rob: int = self.source[31] if self.source[31] is not None else 0
        self.shield_count: int = self.source[32]

        self.autonalogs = bool(self.source[33])
        self.skin: int = self.source[34]
        self.ban = bool(self.source[35])

        d = self.donate
        if d:
            if first_name:
                first_name = d.prefix + ' ' + first_name
            if self.name and d.prefix not in self.name:
                self.name = d.prefix + ' ' + re.sub(r'[^a-zA-Zа-яА-Я0-9]', '', self.name)
        elif self.prefix:
            if self.name and self.prefix not in self.name:
                self.name = self.prefix + ' ' + re.sub(r'[^a-zA-Zа-яА-Я0-9]', '', self.name)
            elif first_name and self.prefix not in first_name:
                first_name = self.prefix + ' ' + first_name

        Thread(target=self.check_names, args=(first_name, username,)).start()

    async def banf(self, reason: str, admin: User, bot: Bot):
        if self.ban:
            return
        self.edit('ban', True)
        try:
            return await bot.send_message(chat_id=self.id,
                                          text=f'⛔ Вы были заблокированы в боте навсегда!\nПричина:\n<code>'
                                               f'{reason}</code>\n🅰️ Администратор: {admin.link}')
        except:
            return

    @property
    def donate(self):
        res = Donate(self.donate_source) if self.donate_source else None
        if res and (res.to_date - datetime.now()).total_seconds() > 1:
            return res
        return None

    def get_bonus(self, first_name=None):
        bonus = config.bonus if not self.donate else self.donate.cash + config.bonus
        if '@barleygamebot' in str(first_name).lower():
            bonus += bonus * 0.25
        self.editmany(balance=self.balance + bonus, bonus=datetime.now().strftime('%d-%m-%Y %H:%M:%S'))
        return bonus

    def get_item(self, item_index: int = None, item_id: int = None):
        if item_id is not None:
            item = None
            for ind, i in enumerate(self.items):
                if item_id == i[0]:
                    item = i
                    break
            if item:
                return item
        else:
            return self.items[item_index]

    def set_item(self, item_index: int = None, item_id: int = None, x: int = 1):
        if item_id is not None:
            item = None
            for ind, i in enumerate(self.items):
                if item_id == i[0]:
                    item = i
                    break
            if item is None:
                self.items.append([item_id, 0])
                item = [item_id, 0]
                ind = len(self.items) - 1
            self.items[ind] = [item_id, item[1] + x]
            if (item[1] + x) <= 0:
                self.items.remove(self.items[ind])
            self.edit('items', ','.join(f'{x[0]}:{x[1]}' for x in self.items), False)
        else:
            a = self.items[item_index]
            if (a[1] + x) <= 0:
                self.items.remove(a)
            else:
                self.items[item_index] = [a[0], a[1] + x]
            self.edit('items', ','.join(f'{x[0]}:{x[1]}' for x in self.items), False)

    def set_item_many(self, item_indexes: list = None, item_ids: list = None, counts: list = None):
        if item_ids is not None:
            for item_id_index, item_id in enumerate(item_ids):
                item = None
                for ind, i in enumerate(self.items):
                    if item_id == i[0]:
                        item = i
                        break
                if item is None:
                    self.items.append([item_id, 0])
                    item = [item_id, 0]
                    ind = len(self.items) - 1
                self.items[ind] = [item_id, item[1] + counts[item_id_index]]
                if (item[1] + counts[item_id_index]) <= 0:
                    self.items.remove(self.items[ind])
            self.edit('items', ','.join(f'{x[0]}:{x[1]}' for x in self.items), False)
        else:
            for item_index_index, item_index in enumerate(item_indexes):
                a = self.items[item_index]
                if (a[1] + counts[item_index_index]) <= 0:
                    self.items.remove(a)
                else:
                    self.items[item_index] = [a[0], a[1] + counts[item_index_index]]
            self.edit('items', ','.join(f'{x[0]}:{x[1]}' for x in self.items), False)

    @property
    def text(self):
        xd = f'({timetomin(int(time.time() - self.deposit_date))})' if self.deposit_date is not None else ''
        x2 = f'({timetomin(int(time.time() - self.credit_time))})' if self.credit_time is not None else ''
        return f'👤 Профиль пользователя: {self.link}\n\n' \
               f'• 💸 Баланс: {to_str(self.balance)}\n' \
               f'• 💳 В банке: {to_str(self.bank)}\n' \
               f'• 🔓 Кредит: {to_str(self.credit)} {x2}\n' \
               f'• 💶 Депозит: {to_str(self.deposit)} {xd}\n' \
               f'• 🪙 Коины: {to_str(self.coins)}\n\n' \
               f'💲 В сумме: {to_str(self.balance + self.bank + self.deposit)}'

    @property
    def link(self):
        url = f'https://t.me/{self.username}' if self.username else f'tg://user?id={self.id}' if self.notifies else \
            f'tg://openmessage?user_id={self.id}'
        return f'<a href="{url}">{self.name if self.name else self.first_name}</a>'

    def check_names(self, first_name, username):
        if first_name:
            if self.first_name != first_name and self.username != username:
                return self.editmany(first_name=first_name, username=username)
            elif self.first_name != first_name:
                return self.edit('first_name', first_name)
            elif self.username != username:
                return self.edit('username', username)

    def edit(self, name, value, attr=True):
        if attr:
            setattr(self, name, value)
        sql.edit_data('id', self.id, name, value)
        return value

    def editmany(self, attr=True, **kwargs):
        items = kwargs.items()
        query = 'UPDATE users SET '
        items_len = len(items)
        for index, item in enumerate(items):
            if attr:
                setattr(self, item[0], item[1])
            query += f'{item[0]} = {sql.item_to_sql(item[1])}'
            query += ', ' if index < items_len - 1 else ' '
        query += 'WHERE id = {}'.format(self.id)
        sql.execute(query=query, commit=True)

    def set_prefix(self, prefix: dict):
        self.editmany(balance=self.balance - prefix['price'],
                      prefix=prefix['emoji'])
        return True
