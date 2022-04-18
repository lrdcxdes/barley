import random
import time
from datetime import datetime

from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from config import donates, set_bitcoin_price, bitcoin_price, uah_price, set_uah_price, set_euro_price, euro_price
from loader import bot
from utils.jobs.jobs import jobs, levels
from utils.main.bitcoin import bitcoins
from utils.main.cars import cars
from utils.main.cash import to_str
from utils.main.db import sql
from utils.main.houses import houses
from utils.main.businesses import businesses
from threading import Lock
from utils.promo.promo import Promocode
from utils.main.moto import motos
from utils.main.rockets import rockets
from utils.countries import countries
import random
import string
from utils.main.users import all_users

lock = Lock()


def deposit_check():
    try:
        with lock:
            cursor = sql.conn.cursor()

            query = ''

            data = sql.execute('SELECT id, donate_source, deposit FROM users WHERE donate_source'
                               f' IS NOT NULL AND ({time.time()} - deposit_date) >= 3600',
                               False, True)
        for i in data:
            x = i[1].split(',')
            date = datetime.strptime(x[1], '%d-%m-%Y %H:%M')
            if (datetime.now() - date).total_seconds() > 1:
                item = donates[int(x[0])]
                dep = i[2]
                xd = 5 if dep < 100000000 else 4 if dep < 1000000000 else 3 if dep < 10000000000 else \
                    2 if dep < 100000000000 else 1 if dep >= 100000000000 else 5
                query += f'UPDATE users SET deposit = deposit + cast(ROUND' \
                         f'(deposit * (percent + {xd} + {item["percent"]})/100) as integer),' \
                         f' deposit_date = {time.time()} WHERE id = {i[0]};\n'
        with lock:
            sql.executescript(cursor=cursor,
                              commit=True,
                              query=query)
        query = f'UPDATE users SET deposit_date = {time.time()}, deposit = deposit +' \
                'cast(ROUND(deposit * (percent + 1)/' \
                '100) as integer)' \
                f' WHERE deposit_date IS NOT ' \
                f'NULL AND ' \
                f'({time.time()} - deposit_date) >= 3600 AND deposit >= 100000000000;\n'
        query += f'UPDATE users SET deposit_date = {time.time()}, deposit = deposit +' \
                 'cast(ROUND(deposit * (percent + 2)/100) as integer)' \
                 f' WHERE deposit_date IS NOT ' \
                 f'NULL AND ' \
                 f'({time.time()} - deposit_date) >= 3600 AND deposit < 100000000000 AND deposit > 10000000000;\n'
        query += f'UPDATE users SET deposit_date = {time.time()}, deposit = deposit +' \
                 'cast(ROUND(deposit * (percent + 3)/' \
                 '100) as integer)' \
                 f' WHERE deposit_date IS NOT ' \
                 f'NULL AND ' \
                 f'({time.time()} - deposit_date) >= 3600 AND deposit < 10000000000 AND deposit > 1000000000;\n'
        query += f'UPDATE users SET deposit_date = {time.time()}, deposit = deposit +' \
                 'cast(ROUND(deposit * (percent + 4)/' \
                 '100) as integer)' \
                 f' WHERE deposit_date IS NOT ' \
                 f'NULL AND ' \
                 f'({time.time()} - deposit_date) >= 3600 AND deposit > 100000000 AND deposit < 1000000000;\n'

        query += f'UPDATE users SET deposit_date = {time.time()}, deposit = deposit +' \
                 'cast(ROUND(deposit * (percent + 5)/' \
                 '100) as integer)' \
                 f' WHERE deposit_date IS NOT ' \
                 f'NULL AND deposit > 0 AND ' \
                 f'({time.time()} - deposit_date) >= 3600 AND deposit <= 100000000;\n'

        with lock:
            sql.executescript(cursor=cursor,
                              commit=True,
                              query=query)
        query = f'UPDATE users SET credit_time = {time.time()}, bank = bank - cast(ROUND(credit / 10, ' \
                f'0) as int) ' \
                f'WHERE credit_time IS NOT NULL AND ({time.time()} - credit_time) >= 7200;\n'

        query += f'UPDATE users SET energy = energy + 1, energy_time = {time.time()}' \
                 f' WHERE energy < 10 AND energy_time IS NOT NULL AND (' \
                 f'{time.time()} - energy_time) >= 3600;'
        with lock:
            sql.executescript(query, commit=True, cursor=cursor)
        return True
    except Exception as ex:
        print(123, ex)


def check_jobs():
    try:
        with lock:
            cursor = sql.conn.cursor()

            query = 'SELECT id, job_index, level FROM users WHERE work_time' \
                    f' IS NOT NULL AND (job_index > 0 OR (level > 6 AND level < 12)) AND ({time.time()} - ' \
                    f'work_time) >= 3600'
            users = sql.execute(query,
                                False, True, cursor)

        query = f'UPDATE users SET job_time = {time.time()}, level = level + 1 WHERE ({time.time()} - job_time) >= ' \
                f'43200;\n'

        for user in users:
            uid, index, level = user
            job = jobs[index] if index > 0 else levels[level]
            query += f'UPDATE users SET work_time = {time.time()}, bank = bank + {job["doxod"]} WHERE id = {uid};\n'

        with lock:
            sql.executescript(cursor=cursor,
                              query=query,
                              commit=True,
                              fetch=False)
    except Exception as ex:
        print(64, ex)


async def cars_check():
    try:
        cursor = sql.conn.cursor()

        query2 = f'SELECT id, "index", nalog, owner FROM cars WHERE last is NOT NULL AND ' \
                 f'({time.time()} - last) >= ' \
                 f'3600 AND energy < 10'
        with lock:
            result = sql.execute(query2, False, True, cursor=cursor)

        query3 = ''

        for car_s in result:
            ids, index, nalog, owner = car_s
            car = cars[index]
            if nalog + car["nalog"] > car['limit']:
                query3 += f'DELETE FROM cars WHERE id = {ids};\n'
                try:
                    await bot.send_message(chat_id=owner, text=f'<b>❗ Ваша машина был продан, потому-что вы не '
                                                               f'оплачивали '
                                                               f'налоги!</b>')
                except:
                    pass
            else:
                query3 += f'UPDATE cars SET nalog = nalog + {car["nalog"]}, ' \
                          f'last = {time.time()}, energy = energy + 1 WHERE id = {ids};\n'
        with lock:
            sql.executescript(query3, True, False, cursor=cursor)
    except Exception as ex:
        print(123, ex)


async def houses_check():
    try:
        cursor = sql.conn.cursor()

        query2 = f'SELECT id, "index", nalog, owner FROM houses WHERE arenda IS TRUE AND last is NOT NULL AND ' \
                 f'({time.time()} - last) >= ' \
                 f'3600'
        with lock:
            result = sql.execute(query2, False, True, cursor=cursor)

        query3 = ''

        for house_s in result:
            ids, index, nalog, owner = house_s
            house = houses[index]
            if nalog + house["nalog"] > house['limit']:
                query3 += f'DELETE FROM houses WHERE id = {ids};\n'
                try:
                    await bot.send_message(chat_id=owner, text=f'<b>❗ Ваш дом был продан, потому-что вы не оплачивали '
                                                               f'налоги!</b>')
                except:
                    pass
            else:
                query3 += f'UPDATE houses SET cash = cash + {house["doxod"]}, nalog = nalog + {house["nalog"]}, ' \
                          f'last = {time.time()} WHERE id = {ids};\n'

        with lock:
            sql.executescript(query3, True, False, cursor=cursor)
    except Exception as ex:
        print(123, ex)


async def businesses_check():
    try:
        cursor = sql.conn.cursor()

        query2 = f'SELECT id, "index", nalog, owner FROM businesses WHERE arenda IS TRUE AND last is NOT NULL AND ' \
                 f'({time.time()} - last) >= ' \
                 f'3600'
        with lock:
            result = sql.execute(query2, False, True, cursor=cursor)

        query3 = ''

        for house_s in result:
            ids, index, nalog, owner = house_s
            business = businesses[index]
            if nalog + business["nalog"] > business['limit']:
                query3 += f'DELETE FROM businesses WHERE id = {ids};\n'
                try:
                    await bot.send_message(chat_id=owner, text=f'<b>❗ Ваш бизнес был продан, потому-что вы не '
                                                               f'оплачивали '
                                                               f'налоги!</b>')
                except:
                    pass
            else:
                query3 += f'UPDATE businesses SET cash = cash + {business["doxod"]}, nalog = nalog +' \
                          f' {business["nalog"]}, ' \
                          f'last = {time.time()} WHERE id = {ids};\n'
        with lock:
            sql.executescript(query3, True, False, cursor=cursor)
    except Exception as ex:
        print(123, ex)


async def yaxti_check():
    try:
        cursor = sql.conn.cursor()

        query2 = f'SELECT id, "index", nalog, owner FROM yaxti WHERE last is NOT NULL AND ' \
                 f'({time.time()} - last) >= ' \
                 f'3600 AND energy < 10'
        with lock:
            result = sql.execute(query2, False, True, cursor=cursor)

        query3 = ''

        for car_s in result:
            ids, index, nalog, owner = car_s
            car = cars[index]
            if nalog + car["nalog"] > car['limit']:
                query3 += f'DELETE FROM yaxti WHERE id = {ids};\n'
                try:
                    await bot.send_message(chat_id=owner, text=f'<b>❗ Ваша машина был продан, потому-что вы не '
                                                               f'оплачивали '
                                                               f'налоги!</b>')
                except:
                    pass
            else:
                query3 += f'UPDATE yaxti SET nalog = nalog + {car["nalog"]}, ' \
                          f'last = {time.time()}, energy = energy + 1 WHERE id = {ids};\n'
        with lock:
            sql.executescript(query3, True, False, cursor=cursor)
    except Exception as ex:
        print(123, ex)


async def tanki_check():
    try:
        cursor = sql.conn.cursor()

        query2 = f'SELECT id, "index", nalog, owner FROM tanki WHERE last is NOT NULL AND ' \
                 f'({time.time()} - last) >= ' \
                 f'3600 AND energy < 10'
        with lock:
            result = sql.execute(query2, False, True, cursor=cursor)

        query3 = ''

        for car_s in result:
            ids, index, nalog, owner = car_s
            car = cars[index]
            if nalog + car["nalog"] > car['limit']:
                query3 += f'DELETE FROM tanki WHERE id = {ids};\n'
                try:
                    await bot.send_message(chat_id=owner, text=f'<b>❗ Ваша машина был продан, потому-что вы не '
                                                               f'оплачивали '
                                                               f'налоги!</b>')
                except:
                    pass
            else:
                query3 += f'UPDATE tanki SET nalog = nalog + {car["nalog"]}, ' \
                          f'last = {time.time()}, energy = energy + 1 WHERE id = {ids};\n'
        with lock:
            sql.executescript(query3, True, False, cursor=cursor)
    except Exception as ex:
        print(123, ex)


async def vertoleti_check():
    try:
        cursor = sql.conn.cursor()

        query2 = f'SELECT id, "index", nalog, owner FROM vertoleti WHERE last is NOT NULL AND ' \
                 f'({time.time()} - last) >= ' \
                 f'3600 AND energy < 10'
        with lock:
            result = sql.execute(query2, False, True, cursor=cursor)

        query3 = ''

        for car_s in result:
            ids, index, nalog, owner = car_s
            car = cars[index]
            if nalog + car["nalog"] > car['limit']:
                query3 += f'DELETE FROM vertoleti WHERE id = {ids};\n'
                try:
                    await bot.send_message(chat_id=owner, text=f'<b>❗ Ваша машина был продан, потому-что вы не '
                                                               f'оплачивали '
                                                               f'налоги!</b>')
                except:
                    pass
            else:
                query3 += f'UPDATE vertoleti SET nalog = nalog + {car["nalog"]}, ' \
                          f'last = {time.time()}, energy = energy + 1 WHERE id = {ids};\n'
        with lock:
            sql.executescript(query3, True, False, cursor=cursor)
    except Exception as ex:
        print(123, ex)


async def airplanes_check():
    try:
        cursor = sql.conn.cursor()

        query2 = f'SELECT id, "index", nalog, owner FROM airplanes WHERE last is NOT NULL AND ' \
                 f'({time.time()} - last) >= ' \
                 f'3600 AND energy < 10'
        with lock:
            result = sql.execute(query2, False, True, cursor=cursor)

        query3 = ''

        for car_s in result:
            ids, index, nalog, owner = car_s
            car = cars[index]
            if nalog + car["nalog"] > car['limit']:
                query3 += f'DELETE FROM airplanes WHERE id = {ids};\n'
                try:
                    await bot.send_message(chat_id=owner, text=f'<b>❗ Ваша самолёт был продан, потому-что вы не '
                                                               f'оплачивали '
                                                               f'налоги!</b>')
                except:
                    pass
            else:
                query3 += f'UPDATE airplanes SET nalog = nalog + {car["nalog"]}, ' \
                          f'last = {time.time()}, energy = energy + 1 WHERE id = {ids};\n'
        with lock:
            sql.executescript(query3, True, False, cursor=cursor)
    except Exception as ex:
        print(123, ex)


async def moto_check():
    try:
        cursor = sql.conn.cursor()

        query2 = f'SELECT id, "index", nalog, owner FROM moto WHERE last is NOT NULL AND ' \
                 f'({time.time()} - last) >= ' \
                 f'3600 AND energy < 10'
        with lock:
            result = sql.execute(query2, False, True, cursor=cursor)

        query3 = ''

        for car_s in result:
            ids, index, nalog, owner = car_s
            car = motos[index]
            if nalog + car["nalog"] > car['limit']:
                query3 += f'DELETE FROM moto WHERE id = {ids};\n'
                try:
                    await bot.send_message(chat_id=owner, text=f'<b>❗ Ваша мотоцикл был продан, потому-что вы не '
                                                               f'оплачивали '
                                                               f'налоги!</b>')
                except:
                    pass
            else:
                query3 += f'UPDATE moto SET nalog = nalog + {car["nalog"]}, ' \
                          f'last = {time.time()}, energy = energy + 1 WHERE id = {ids};\n'
        with lock:
            sql.executescript(query3, True, False, cursor=cursor)
    except Exception as ex:
        print(123, ex)


async def rockets_check():
    try:
        cursor = sql.conn.cursor()

        query2 = f'SELECT id, "index", nalog, owner FROM rockets WHERE last is NOT NULL AND ' \
                 f'({time.time()} - last) >= ' \
                 f'3600 AND energy < 10'
        with lock:
            result = sql.execute(query2, False, True, cursor=cursor)

        query3 = ''

        for car_s in result:
            ids, index, nalog, owner = car_s
            car = rockets[index]
            if nalog + car["nalog"] > car['limit']:
                query3 += f'DELETE FROM rockets WHERE id = {ids};\n'
                try:
                    await bot.send_message(chat_id=owner, text=f'<b>❗ Ваша ракета был продан, потому-что вы не '
                                                               f'оплачивали '
                                                               f'налоги!</b>')
                except:
                    pass
            else:
                query3 += f'UPDATE rockets SET nalog = nalog + {car["nalog"]}, ' \
                          f'last = {time.time()}, energy = energy + 1 WHERE id = {ids};\n'
        with lock:
            sql.executescript(query3, True, False, cursor=cursor)
    except Exception as ex:
        print(123, ex)


async def btc_check():
    try:
        cursor = sql.conn.cursor()

        query2 = f'SELECT id, zindex, nalog, owner, videocards FROM bitcoin WHERE last is NOT NULL AND ' \
                 f'({time.time()} - last) >= ' \
                 f'3600'
        with lock:
            result = sql.execute(query2, False, True, cursor=cursor)

        query3 = ''

        for car_s in result:
            ids, index, nalog, owner, videocards = car_s
            car = bitcoins[index]()
            if nalog + car.nalog > car.limit:
                query3 += f'DELETE FROM bitcoin WHERE id = {ids};\n'
                try:
                    await bot.send_message(chat_id=owner, text=f'<b>❗ Ваша ферма был продан, потому-что вы не '
                                                               f'оплачивали '
                                                               f'налоги!</b>')
                except:
                    pass
            else:
                summ = car.doxod * videocards
                query3 += f'UPDATE bitcoin SET nalog = nalog + {car.nalog}, ' \
                          f'last = {time.time()}, balance = ROUND(balance + {summ}, 8) WHERE id ' \
                          f'= {ids};\n'
        with lock:
            sql.executescript(query3, True, False, cursor=cursor)
    except Exception as ex:
        print(123, ex)


async def btc_change():
    x = bitcoin_price() * float(f'0.0{random.randint(0, 5)}') if bitcoin_price() < 100000 else bitcoin_price() * \
                                                                                               float(
                                                                                                   f'0.00{random.randint(0, 5)}')
    now = random.choice([int(bitcoin_price() + x), int(bitcoin_price() - x)])
    if now != bitcoin_price():
        await set_bitcoin_price(now)

    x = euro_price() * float(f'0.0{random.randint(0, 5)}') if euro_price() < 100000 else euro_price() * \
                                                                                         float(
                                                                                             f'0.00{random.randint(0, 5)}')
    now = random.choice([int(euro_price() + x), int(euro_price() - x)])
    if now != euro_price():
        await set_euro_price(now)

    x = uah_price() * float(f'0.0{random.randint(0, 5)}') if uah_price() < 100000 else uah_price() * \
                                                                                       float(
                                                                                           f'0.00{random.randint(0, 5)}')
    now = random.choice([int(uah_price() + x), int(uah_price() - x)])
    if now != uah_price():
        await set_uah_price(now)


name_by_index = ['cars', 'airplanes', 'houses', 'businesses',
                 'moto', 'tanki', 'vertoleti', 'yaxti', 'rockets', 'bitcoin']


def autonalog_check():
    with lock:
        query = 'SELECT id, bank FROM users WHERE autonalogs IS TRUE AND bank > 1000'
        data = sql.execute(query, False, True)
        query = ''
        for user_id, bank in data:
            owner = user_id
            data = []
            for i in name_by_index:
                x = sql.execute(f'SELECT nalog FROM {i} WHERE owner = {owner}',
                                False, True)
                data.append(x[0][0] if len(x) > 0 else None)
            if len(data) == 0:
                continue
            nalog = data
            nalog_summ = sum(i for i in nalog if i is not None)

            if nalog_summ > bank or nalog_summ == 0:
                continue

            query += f'UPDATE users SET bank = bank - {nalog_summ} WHERE id = {owner};\n'

            for index, value in enumerate(nalog):
                if value is not None:
                    query += f'UPDATE {name_by_index[index]} SET nalog = 0 WHERE owner = {owner};\n'

        sql.executescript(query, True, False)


async def autopromo_handler():
    balance = sql.execute('SELECT balance FROM users WHERE "id" = 5162113453', False, True)[0][0]
    if balance < (100000 * len(all_users())):
        return
    price = 100000
    acts = len(all_users())

    name = ''.join(random.choice(string.ascii_letters + '0123456789_') for _ in range(random.randint(6, 16))).lower()

    Promocode.create(name=name,
                     activations=acts,
                     summ=price,
                     xd=1)
    sql.execute(f'UPDATE users SET balance = balance - {price * acts} WHERE "id" = 5162113453', True, False)

    try:
        await bot.send_message(
            text=f'🤭 Новый промокод <code>{name}</code> на сумму {to_str(price)} и кол-во активаций {acts}',
            chat_id=-1001751575344)
    except:
        return


def countries_check():
    xd = list(countries().items())
    for index, country in xd:
        if country.army.status:
            country.edit('balance', country.balance - random.randint(1000, 10000))
        if country.soyuz:
            country.edit('balance', country.balance + 10000)
        if not country.war:
            continue
        if (time.time() - country.war_time) < 3600:
            xax = random.choice(['rockets', 'snaraj', 'tech'])
            name = getattr(country.army, xax)
            if name > 0:
                country.army.edit(xax, name - random.randint(1, 5))
            xax = random.choice(['rockets', 'snaraj', 'tech'])
            name = getattr(country.war.army, xax)
            if name > 0:
                country.war.army.edit(xax, name - random.randint(1, 5))
            wars = [True, False]
            chances = [50, 50]
            summ = sum(len(str(x)) for x in [country.army.rockets, country.army.snaraj, country.army.tech])
            summ += 2 if country.army.status else 0
            alls = 0
            for i in countries().values():
                alls += sum(len(str(x)) for x in [i.army.rockets, i.army.snaraj, i.army.tech])
                alls += 2 if i.army.status else 0
            chances[0] += int((summ / alls) * 100)
            choice1 = random.choices(wars, weights=tuple(chances), k=1)[0]
            if choice1:
                x = random.randint(1, 5)
                country.edit('territory', country.territory + x)
                if (country.war.territory - x) >= 0:
                    country.war.edit('territory', country.war.territory - x)
                elif country.war.territory == 0:
                    pass
                else:
                    country.war.edit('territory', 0)
                try:
                    xd.remove((index, country.war))
                except:
                    pass
            elif not choice1 and (country.war.army.tech + country.war.army.snaraj + country.war.army.rockets) > 0:
                x = random.randint(1, 5)
                country.war.edit('territory', country.war.territory + x)
                if (country.territory - x) >= 0:
                    country.edit('territory', country.territory - x)
                elif country.territory == 0:
                    pass
                else:
                    country.edit('territory', 0)
                try:
                    xd.remove((index, country))
                except:
                    pass
        else:
            country.war.editmany(war=None, war_time=None)
            country.editmany(war=None, war_time=None)


autopromo_s = AsyncIOScheduler()
autopromo_s.add_job(autopromo_handler, 'cron', hour='*')
autopromo_s.start()

countries_s = BackgroundScheduler()
countries_s.add_job(countries_check, 'cron', minute='*')
countries_s.start()

deposit_scheduler = BackgroundScheduler()
deposit_scheduler.add_job(deposit_check, 'cron', minute='*')
deposit_scheduler.start()

autonalog_scheduler = BackgroundScheduler()
autonalog_scheduler.add_job(autonalog_check, 'cron', minute='*')
autonalog_scheduler.start()

houses_scheduler = AsyncIOScheduler()
houses_scheduler.add_job(houses_check, 'cron', minute='*')
houses_scheduler.start()

businesses_scheduler = AsyncIOScheduler()
businesses_scheduler.add_job(businesses_check, 'cron', minute='*')
businesses_scheduler.start()

cars_scheduler = AsyncIOScheduler()
cars_scheduler.add_job(cars_check, 'cron', minute='*')
cars_scheduler.start()

yaxti_scheduler = AsyncIOScheduler()
yaxti_scheduler.add_job(yaxti_check, 'cron', minute='*')
yaxti_scheduler.start()

tanki_scheduler = AsyncIOScheduler()
tanki_scheduler.add_job(tanki_check, 'cron', minute='*')
tanki_scheduler.start()

vertoleti_scheduler = AsyncIOScheduler()
vertoleti_scheduler.add_job(vertoleti_check, 'cron', minute='*')
vertoleti_scheduler.start()

airplanes_scheduler = AsyncIOScheduler()
airplanes_scheduler.add_job(airplanes_check, 'cron', minute='*')
airplanes_scheduler.start()

moto_scheduler = AsyncIOScheduler()
moto_scheduler.add_job(moto_check, 'cron', minute='*')
moto_scheduler.start()

rockets_scheduler = AsyncIOScheduler()
rockets_scheduler.add_job(rockets_check, 'cron', minute='*')
rockets_scheduler.start()

btc_scheduler = AsyncIOScheduler()
btc_scheduler.add_job(btc_check, 'cron', minute='*')
btc_scheduler.start()

check_jobs_s = BackgroundScheduler()
check_jobs_s.add_job(check_jobs, 'cron', minute='*')
check_jobs_s.start()

btc_change_s = AsyncIOScheduler()
btc_change_s.add_job(btc_change, 'cron', hour='*')
btc_change_s.start()
