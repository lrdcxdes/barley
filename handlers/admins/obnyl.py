from aiogram.types import Message

from utils.main.db import sql


async def obnyn_handler(message: Message):
    query = 'UPDATE users SET balance = 0, bank = 0, deposit = 0, pets = "", items = "", deposit_date = NULL, ' \
            'bonus = 01-01-2000 00:00:00, lock = FALSE, credit = 0, credit_time = NULL, energy = 10, energy_time = ' \
            'NULL, xp = 0, sell_count = 0, level = 0, job_index = 0, job_time = NULL,' \
            ' work_time = NULL, prefix = NULL, admin_last = NULL,' \
            ' last_rob = NULL, shield_count = 0, autonalogs = FALSE, skin = NULL, ban = FALSE'

    donate = len(message.text.split()) > 1

    if donate:
        query += ', percent = 0, coins = 0, donate_source = NULL;\n'
    else:
        query += ';\n'

    query += 'DELETE FROM airplanes;\n' \
             'DELETE FROM bitcoin;\n' \
             'DELETE FROM businesses;\n' \
             'DELETE FROM cars;\n' \
             'DELETE FROM countries;\n' \
             'DELETE FROM euro;\n' \
             'DELETE FROM houses;\n' \
             'DELETE FROM marries;\n' \
             'DELETE FROM moto;\n' \
             'DELETE FROM promocodes;\n' \
             'DELETE FROM rockets;\n' \
             'DELETE FROM tanki;\n' \
             'DELETE FROM uah;\n' \
             'DELETE FROM vertoleti;\n' \
             'DELETE FROM yaxti;' \

    sql.executescript(query, True, False)

    return await message.reply('[👨‍🎤] Обнуление прошло успешно!')
