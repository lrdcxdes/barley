from datetime import datetime, timedelta
from config import donates


def to_str(result: timedelta):
    days = result.days
    hours, remainder = divmod(result.seconds, 3600)
    minutes, seconds = divmod(remainder, 60)

    res = ''
    if days > 0:
        res += f'{days} д.'
    if hours > 0:
        res += f' {hours} ч.'
    if minutes > 0:
        res += f' {minutes} м.'
    if seconds > 0:
        res += f' {seconds} с.'
    return res if res else 'Неизвестно'


class Donate:
    def __init__(self, source: str):
        self.split = source.split(',')

        self.id: int = int(self.split[0])

        self.start_date: datetime = datetime.strptime(self.split[1], '%d-%m-%Y %H:%M')

        xd = donates[self.id]
        self.to_date: datetime = self.start_date + timedelta(days=30)
        self.left: timedelta = self.to_date - self.start_date
        self.left_str: str = to_str(self.left)
        self.name: str = xd['name']
        self.price: int = xd["price"]
        self.prefix: str = xd["prefix"]
        self.cash: int = xd['cash']
        self.percent: int = xd['percent']
