import logging
import sqlite3
from datetime import datetime

from config import database, log

from threading import Lock, Thread


if log:
    lastdate = datetime.now().strftime("%d.%m.%y")
    logger = logging.getLogger('log_db')
    logger.setLevel(logging.INFO)
    fh = logging.FileHandler(f'assets/logs/{lastdate}.log', mode='a')
    fh.setLevel(logging.INFO)
    formatter = logging.Formatter(
            '[%(asctime)s] %(message)s', datefmt='%H:%M:%S')
    fh.setFormatter(formatter)
    logger.addHandler(fh)


def new_file():
    if not log:
        return
    global lastdate, fh

    lastdate = datetime.now().strftime("%d.%m.%y")
    try:
        logger.removeHandler(fh)
    except:
        pass
    fh = logging.FileHandler(f'assets/logs/{lastdate}.log', mode='a')
    fh.setLevel(logging.INFO)
    formatter = logging.Formatter(
        '[%(asctime)s] %(message)s', datefmt='%H:%M:%S')
    fh.setFormatter(formatter)
    logger.addHandler(fh)


def axaxaxax(action: str, text: str):
    if lastdate != datetime.now().strftime("%d.%m.%y") or logger is None:
        new_file()
    logger.info(f'({action}): {text}')


def write_admins_log(action: str, text: str):
    if not log:
        return
    Thread(target=axaxaxax, args=(action, text)).start()


lock = Lock()


def timetomin(result: int):
    result = 3600 - result
    minutes = int((result // 60) % 60)
    return f'{minutes} мин.'


def timetostr(result: int):
    a = int(result // 3600)
    b = int((result % 3600) // 60)
    c = int((result % 3600) % 60)

    res = ''
    if a > 0:
        res += f'{a} ч.'
    if b > 0:
        res += f' {b} м.'
    if c > 0:
        res += f' {c} с.'
    return res if res else 'Неизвестно'


class Lsql:
    def __init__(self, file):
        f = file[::-1]
        if f[:4] == "db.":
            f = f[4:]
            file = f[::-1]
        self.conn = sqlite3.connect(f"{file}.db", check_same_thread=False)
        self.cursor = self.conn.cursor()

    def insert_data(self, data_mass, table="users"):
        len_title = "?," * (len(list(data_mass[0])) - 1) + "?"
        with lock:
            self.cursor.executemany(f"INSERT INTO {table} VALUES ({len_title})", data_mass)
            self.conn.commit()
        write_admins_log(f'INSERT `{table}`', f'{data_mass[0]}')

    def edit_data(self, title_last, last, title_new, new, table="users"):
        with lock:
            self.cursor.execute(f"UPDATE {table} SET {title_new} = ? WHERE {title_last} = ?",
                            [(new), (last)])
            self.conn.commit()
        write_admins_log(f'EDIT `{table}`', f'INFO - {title_last} = {last} DATA - {title_new} = {new}')

    def delete_data(self, name, title_name, table="users"):
        with lock:
            self.cursor.execute(f"DELETE FROM {table} WHERE {title_name} = ?", [(name)])
            self.conn.commit()
        write_admins_log(f'DELETE `{table}`', f'INFO - {title_name} = {name}')

    def select_data(self, name, title, row_factor=False, table="users"):
        with lock:
            self.cursor.execute(f"SELECT * FROM {table} WHERE {title}=?", [(name)])
        if row_factor:
            with lock:
                return self.cursor.fetchone()
        else:
            with lock:
                return self.cursor.fetchall()

    def search(self, type_search, name_search, table="users"):
        with lock:
            self.cursor.execute(f"SELECT * FROM {table} WHERE {type_search} LIKE {name_search}")
            return self.cursor.fetchall()

    def get_all_data(self, table="users"):
        with lock:
            self.cursor.execute(f"SELECT * FROM {table}")
            return self.cursor.fetchall()

    def execute(self, query: str, commit: bool = False, fetch: bool = False, cursor=None):
        if cursor is None:
            cursor = self.cursor
        with lock:
            cursor.execute(query)
        if commit:
            with lock:
                self.conn.commit()
        with lock:
            write_admins_log(f'EXECUTE', f'{query}')

            return cursor.fetchall() if fetch else None

    def executescript(self, query: str, commit: bool = False, fetch: bool = False, cursor=None):
        if cursor is None:
            cursor = self.cursor
        with lock:
            cursor.executescript(query)
        if commit:
            with lock:
                self.conn.commit()
        with lock:
            write_admins_log(f'EXECUTEMANY', f'{query}')
            return cursor.fetchall() if fetch else None

    def commit(self):
        with lock:
            self.conn.commit()

    def get_cursor(self):
        return self.cursor

    def get_connect(self):
        return self.conn

    def item_to_sql(self, item):
        if type(item) == str:
            return f'"{item}"'
        elif type(item) == bool:
            return 'TRUE' if item else 'FALSE'
        elif item is None:
            return 'NULL'
        else:
            return item


sql = Lsql(database)
