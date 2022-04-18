import asyncio
from hashlib import md5
from threading import Lock

from flask import Flask, request

from config import freekassa_secrets, freekassa_shop_id, freekassa, freekassa_api_key
from loader import bot, owner
from utils.main.users import User


secrets = freekassa_secrets

api = freekassa_api_key

merchant_id = f'{freekassa_shop_id}'

if freekassa:
    app = Flask(__name__)


    @app.route('/payment', methods=['POST'])
    def index():
        if request.remote_addr not in ['168.119.157.136', '168.119.60.227',
                                       '138.201.88.124', '178.154.197.79']:
            return "hacking attempt!"

        sign = merchant_id + \
               ':' + str(request.args.get('AMOUNT')) + \
               ':' + secrets[1] + \
               ':' + str(request.args.get('MERCHANT_ORDER_ID'))

        hash_object = md5(sign.encode()).hexdigest()

        if hash_object != request.args.get('SIGN'):
            return 'wrong sign'

        success(request.args)

        return 'YES'


    async def notify(user_txt: str, admin_txt: str, user: User):
        try:
            await bot.send_message(text=user_txt,
                                   chat_id=user.id)
        except:
            pass

        try:
            await bot.send_message(text=admin_txt,
                                   chat_id=owner)
        except:
            pass


    lock = Lock()


    def success(args: dict):
        summ = args['AMOUNT']
        author = args['payer_account']
        order_id = args['MERCHANT_ORDER_ID']
        with lock:
            user_id = User(id=int(order_id))
            user_id.edit('coins', user_id.coins + summ)

        notify_user = f'✅ Счёт #{order_id} оплачен!\n\n' \
                      f'На ваш баланс зачислено: +{summ} коинов!'

        notify_admin = f'✅ Счёт #{order_id}\n' \
                       f'👤 Платильщик: {user_id.link}\n' \
                       f'💰 Сумма: {summ}RUB\n' \
                       f'📃 Реквизиты платильщика: <code>{author}</code>'

        asyncio.get_event_loop().run_until_complete(notify(notify_user, notify_admin, user_id))


def start():
    if freekassa:
        import logging
        log = logging.getLogger('werkzeug')
        log.setLevel(logging.ERROR)

        app.run(host='0.0.0.0', port=80)
