from __future__ import annotations

import time

from utils.main.cash import to_str
from utils.main.db import sql, timetomin
from utils.main.users import User


class Army:
    def __init__(self, source: str, country: Country):
        split = source.split(',')
        self.tech = int(split[0])
        self.snaraj = int(split[1])
        self.rockets = int(split[2])
        self.status = split[3] == 'True'

        self.country = country

    def edit(self, name, value):
        setattr(self, name, value)
        self.country.edit('army', f'{self.tech},{self.snaraj},{self.rockets},{self.status}', False)
        return value

    @property
    def text(self):
        return f'🛡 Армия страны {self.country.full_name}:\n\n' \
               f'🚃 Техника: <b>{self.tech}</b>\n' \
               f'🔫 Ракеты: <b>{self.rockets}</b>\n' \
               f'🛡️ Снаряжение: <b>{self.snaraj}</b>\n' \
               f'💫 Статус: <b>{"⛔ Готовность" if self.status else "✅ Отдых"}</b>'


countries_ = {}


def countries():
    return countries_


def countriess():
    global countries_
    countries_ = {index: Country(i) for index, i in enumerate(sql.get_all_data('countries'), start=1)}


def set_country(name, value):
    countries_[name] = value


class Country:
    @staticmethod
    def find_country(country: str):
        if country.isdigit():
            return countries().get(int(country))
        for i in countries().values():
            if i.name.lower() in country.lower() or country.lower() in i.name.lower() or \
                    i.emoji in country:
                return i
        return None

    def __init__(self, source: tuple):
        self.source = source

        self.id: int = source[0]
        self.name: str = source[1]
        if self.name[-1] == ' ':
            self.name = self.name[:-1]
        self.emoji: str = source[2]
        self.territory: int = source[3]
        self.owner: int | None = source[4]
        self.soyuz_ = source[5]
        self.users: list = [int(i) for i in source[6].split(',') if i]
        self.balance: int = source[7]
        self.last_owner: int | None = source[8]
        self.army = Army(source[9], self)
        self.war_ = source[10]
        self.war_time: float | None = source[11]

    @property
    def soyuz(self):
        return countries()[self.soyuz_] if type(self.soyuz_) == int else self.soyuz_ if isinstance(self.soyuz_,
                                                                                              Country) else None

    @soyuz.setter
    def soyuz(self, value):
        self.soyuz_ = value

    @property
    def war(self):
        return countries()[self.war_] if type(self.war_) == int else self.war_ if isinstance(self.war_, Country) else None

    @war.setter
    def war(self, value):
        self.war_ = value

    @property
    def owner_link(self):
        return User(id=self.owner).link if self.owner is not None else "НетПрезидента"

    @property
    def full_name(self):
        return f'<b>{self.name} {self.emoji}</b>'

    @staticmethod
    def get_percent(value: int):
        alls = sum(i.territory for i in countries().values())
        try:
            return f'{int((value / alls) * 100)}%'
        except:
            return '0%'

    @property
    def text(self):
        xd = timetomin(int(time.time() - self.war_time)) if self.war_time is not None else ''
        return f'🏴‍☠️ Информация о стране {self.full_name}:\n\n' \
               f'🤑 Президент: {self.owner_link}\n' \
               f'🗾 Территория: <b>{self.territory}</b>км² (<code>{self.get_percent(self.territory)}</code>)\n' \
               f'🤝 Союз: {self.soyuz.full_name if self.soyuz else "Нету ⛔"}\n' \
               f'👥 Население: <b>{len(self.users)}</b> чел.\n' \
               f'💰 Бюджет: {to_str(self.balance)}\n' \
               f'🪖 Война против: {self.war.full_name if self.war else "Никого ⛔"}{xd}\n' \
               f'💥 Военная сила: {self.army_sila}'
    
    @property
    def army_sila(self):
        summ = sum(len(str(i)) for i in [self.army.rockets, self.army.snaraj, self.army.tech])
        summ += 2 if self.army.status else 0
        alls = 0
        for i in countries().values():
            alls += sum(len(str(x)) for x in [i.army.rockets, i.army.snaraj, i.army.tech])
            alls += 2 if i.army.status else 0
        p = f'{int((summ / alls) * 100)}%'
        return f'<b>{p}</b>'

    @staticmethod
    def get_top(limit: int = 5):
        x = list(countries().items())
        x.sort(key=lambda z: z[1].territory, reverse=True)
        return x[:limit]

    def edit(self, name, value, attr=True):
        if attr:
            setattr(self, name, value)
        sql.edit_data('id', self.id, name, value, 'countries')
        return value

    def editmany(self, attr=True, **kwargs):
        items = kwargs.items()
        query = 'UPDATE countries SET '
        items_len = len(items)
        for index, item in enumerate(items):
            if attr:
                setattr(self, item[0], item[1])
            query += f'{item[0]} = {sql.item_to_sql(item[1])}'
            query += ', ' if index < items_len - 1 else ' '
        query += 'WHERE id = {}'.format(self.id)
        sql.execute(query=query, commit=True)

    def add_user(self, user_id: int):
        if user_id not in self.users:
            self.users.append(user_id)
            self.edit('users', ','.join(str(x) for x in self.users if x), False)

    def del_user(self, user_id: int):
        if user_id in self.users:
            self.users.remove(user_id)
            self.edit('users', ','.join(str(x) for x in self.users if x), False)

    @staticmethod
    def get_by_user(user_id: int):
        for country in countries().values():
            if user_id in country.users:
                return country


countriess()

tech_price = 35000
snaraj_price = 15000
rockets_price = 55000


country_creation_price = 50000000000
