from aiogram.types import ContentType, InputFile, Message

from config import log
from aiogram import Dispatcher

from config import owner_id
from filters.ref import IsRef
from filters.triggers import Trigger
from filters.admin import IsOwner, IsBot
from filters.users import IsPremium, IsAdmin, IsBan
from handlers.admins.ban import ban_user_handler
from handlers.admins.obnyl import obnyn_handler
from handlers.admins.promo import promo_handler
from handlers.admins.rass import (
    rass_menu_handler,
    rass_step2_handler,
    rass_step3_handler,
    rass_finish_handler,
)
from handlers.bot import bot_added_to_chat
from handlers.users.bitcoin.main import (
    bitcoin_handler,
    videocards_handler,
    ferma_handler,
)
from handlers.users.bonus import bonus_handler
from handlers.users.bosses.main import bosses_handler
from handlers.users.businesses.businesses import business_handler
from handlers.users.cars.airplanes import airplanes_handler
from handlers.users.cars.cars import cars_handler
from handlers.users.cars.moto import moto_handler
from handlers.users.cars.rockets import rocket_handler
from handlers.users.cars.tanki import tanki_handler
from handlers.users.cars.vertoleti import vertoleti_handler
from handlers.users.cars.yaxti import yaxti_handler
from handlers.users.cash.bank import bank_handler, credit_handler
from handlers.users.cash.deposit import deposit_handler
from handlers.users.cash.euro import euro_handler
from handlers.users.cash.rob import rob_handler, shield_handler
from handlers.users.cash.uah import uah_handler
from handlers.users.countries.army import (
    army_handler,
    army_tech_handler,
    army_rockets_handler,
    army_snaraj_handler,
    army_gotov_handler,
)
from handlers.users.countries.main import countries_handler, country_create_handler
from handlers.users.countries.my import (
    my_country_handler,
    join_country_handler,
    leave_country_handler,
)
from handlers.users.countries.owners import (
    get_country_handler,
    leave_from_country_handler,
    snyat_budget_country,
    give_budget_country,
)
from handlers.users.countries.soyuz import soyuz_handler, cancel_soyuz_handler
from handlers.users.countries.wars import wars_handler, cancel_wars_handler
from handlers.users.donate import (
    donate_handler,
    zadonatit_handler,
    obmen_handler,
    percent_buy_handler,
    cobmen_handler,
    other_method_handler,
    Payok,
    payok_step1,
    Freekassa,
    freekassa_handler,
    payok_handler,
    freekassa_step1,
    payok_check,
)
from handlers.users.exceptions import errors_handler
from handlers.users.games.bowling import bowling_handler
from handlers.users.games.cases import cases_handler
from handlers.users.games.cnb import cnb_handler
from handlers.users.games.darts import darts_handler
from handlers.users.games.nvuti import nvuti_handler
from handlers.users.games.oreshka import oreshka_handler
from handlers.users.games.roulette import roulette_handler
from handlers.users.games.casino import casino_handler
from handlers.users.games.dice import dice_handler
from handlers.users.houses.houses import house_handler
from handlers.users.items import item_handler
from handlers.users.jobs.jobs import jobs_handler
from handlers.users.main import start_handler, help_handler, help_call_handler
from rich import print

from handlers.users.marries import marry_handler, marry_call_handler
from handlers.users.me import (
    balance_handler,
    nickname_handler,
    notifies_handler,
    profile_handler,
    nedavno_handler,
)
from handlers.users.cash.pay import pay_handler
from handlers.users.nalogs import nalogs_handler, autonalog_handler
from handlers.users.pets import pets_handler
from handlers.users.prefixes import prefix_handler
from handlers.users.promo import activatepromo_handler
from handlers.users.ref import refferal_handler
from handlers.users.rp import emojis, rp_commands_handler
from handlers.users.shop.users import users_shop_handler
from handlers.users.skins import skins_handler, skin_call
from handlers.users.top import top_handler
from handlers.users.works.bottles import bottles_handler
from handlers.users.works.mine import mine_handler
from handlers.users.works.zavod import zavod_handler
from keyboard.main import remove
from states.admins import Rass, ABD
from utils.freekassa import start
from utils.main.users import all_users
from utils.main.chats import all_chats
from handlers.admins.main import (
    givebalance_handler,
    stats_handler,
    plan_bd,
    plan_bd_step1,
    plan_bd_finish,
    plan_bd_step2,
    givedonate_handler,
    privilegia_handler_admin,
    givebalance_admin_handler,
    stats_dop_call,
    get_chat_list,
)
from threading import Thread


async def on_shutdown(dp: Dispatcher):
    print("[red]Bot finished! [blue][•-•][/blue]")


async def on_startup(dp: Dispatcher):
    print("[green]Bot started! [blue][•-•][/blue]")
    await register_handlers(dp)
    Thread(target=start).start()
    if log:
        try:
            await dp.bot.send_message(
                chat_id=owner_id,
                text=f"<b>🪄 Бот запущен!</b> "
                f'<code>{datetime.now().strftime("%d.%m.%y %H:%M:%S")}</code>\n\n'
                f"<b>👥 Пользователей в боте:</b> <code>{len(all_users())}</code>\n"
                f"<b>🛖 Чатов в которых есть бот:</b> <code>"
                f"{len(all_chats())}</code>",
            )
        except Exception as e:
            print(e)


async def calc_handler(message):
    return


from io import StringIO
from contextlib import redirect_stdout


async def eval_handler(message):
    code = message.text.replace("/eval", "").strip()
    try:
        f = StringIO()
        with redirect_stdout(f):
            exec(code)
        out = f.getvalue()
        return await message.reply(str(out).replace("<", "").replace(">", ""))
    except Exception as ex:
        return await message.reply(str(ex).replace(">", "").replace("<", ""))


async def channel_handler(message):
    return


async def cancel_handler(m, state):
    await state.finish()
    return await m.reply(text="Отменено.", reply_markup=remove)


async def echo_handler(m):
    message = m.reply_to_message
    return await message.send_copy(m.from_user.id)


from datetime import datetime
from pytz import timezone


async def time_handler(m):
    kiev = datetime.now()
    moscow = kiev.astimezone(timezone("Europe/Moscow"))
    omsk = kiev.astimezone(timezone("Etc/GMT-6"))

    text = "•-• Текущее время в:\n\n"

    array = {"Киев": kiev, "Москва": moscow, "Омск": omsk}

    for name, timer in array.items():
        time = timer.strftime("%d.%m.%y %H:%M:%S")
        text += f"<b>{name}</b> — <code>{time}</code>\n"

    return await m.reply(text)


async def logs_handler(message: Message):
    try:
        return await message.reply_document(
            document=InputFile(f'assets/logs/{datetime.now().strftime("%d.%m.%y")}.log')
        )
    except:
        return await message.reply("Не удалось отправить логи.")


async def ban_handler(message: Message):
    if message.chat.id == message.from_user.id:
        return await message.reply("⛔ Вы забанены!")


async def register_handlers(dp: Dispatcher):
    # Channel pass
    dp.register_message_handler(
        channel_handler,
        lambda m: m.from_user.id in [777000, 136817688] or m.forward_from,
    )

    dp.register_message_handler(cancel_handler, text="❌", state="*")

    dp.register_message_handler(ban_user_handler, Trigger(["ban", "unban"]), IsOwner())
    dp.register_message_handler(ban_handler, IsBan(), content_types="text", state="*")

    # Adminka
    dp.register_message_handler(
        promo_handler, IsOwner(), commands=["promo", "gift", "promocode"]
    )
    dp.register_message_handler(
        givebalance_handler, IsOwner(), Trigger(["выдать", "give"])
    )

    dp.register_message_handler(
        givebalance_admin_handler, Trigger(["выдать", "give"]), IsAdmin()
    )

    dp.register_message_handler(eval_handler, Trigger(["eval"]), IsOwner())
    dp.register_message_handler(logs_handler, Trigger(["logs"]), IsOwner())
    dp.register_message_handler(obnyn_handler, Trigger(["обнулбота"]), IsOwner())

    dp.register_message_handler(
        stats_handler, IsOwner(), Trigger(["стата", "статистика", "stat", "stats"])
    )

    dp.register_message_handler(
        stats_handler, Trigger(["стата", "статистика", "stat", "stats"]), IsPremium()
    )

    dp.register_callback_query_handler(
        stats_dop_call, IsOwner(), text="statsdop", state="*"
    )

    dp.register_callback_query_handler(
        stats_dop_call, IsPremium(), text="statsdop", state="*"
    )

    dp.register_callback_query_handler(
        rass_menu_handler, IsOwner(), text_startswith="rass_"
    )
    dp.register_message_handler(
        rass_step2_handler, IsOwner(), content_types=ContentType.ANY, state=Rass.post
    )
    dp.register_message_handler(
        rass_step3_handler, IsOwner(), content_types="text", state=Rass.kb
    )
    dp.register_message_handler(
        rass_finish_handler, IsOwner(), content_types="text", state=Rass.time
    )

    dp.register_callback_query_handler(
        get_chat_list, IsOwner(), text="allchats", state="*"
    )

    dp.register_callback_query_handler(plan_bd, IsOwner(), text="plan", state="*")
    dp.register_message_handler(plan_bd_step1, IsOwner(), state=ABD.start)
    dp.register_message_handler(plan_bd_step2, IsOwner(), state=ABD.step_1)
    dp.register_message_handler(plan_bd_finish, IsOwner(), state=ABD.step_2)

    dp.register_message_handler(
        givedonate_handler, IsOwner(), Trigger(["gdonate", "ддонат", "гдонат"])
    )
    dp.register_message_handler(
        privilegia_handler_admin,
        IsOwner(),
        Trigger(["дприву", "гприву", "дприва", "гприва"]),
    )

    # Main commands
    dp.register_message_handler(echo_handler, commands="echo", state="*")

    dp.register_message_handler(
        bot_added_to_chat, IsBot(), content_types="new_chat_members"
    )
    dp.register_message_handler(start_handler, IsRef(), commands="start")
    dp.register_message_handler(
        start_handler, commands="start", commands_prefix=["!", "/", "."]
    )
    dp.register_message_handler(help_handler, Trigger(["помощь", "help"]))
    dp.register_callback_query_handler(
        help_call_handler, text_startswith="help_", state="*"
    )
    dp.register_message_handler(calc_handler, Trigger(["calc", "рассчитать"]))

    # Exceptions
    dp.register_errors_handler(errors_handler)

    # Profile commands
    dp.register_message_handler(
        balance_handler, Trigger(["б", "баланс", "balance", "b"])
    )
    dp.register_message_handler(
        profile_handler, Trigger(["профиль", "me", "профайл", "п"])
    )
    dp.register_message_handler(
        nickname_handler, Trigger(["ник", "nick", "nickname", "name", "никнейм"])
    )
    dp.register_message_handler(
        notifies_handler, Trigger(["уведы", "notifies", "notify", "уведомления"])
    )

    # Top system
    dp.register_message_handler(top_handler, Trigger(["топ", "top"]))

    # Bank commands
    dp.register_message_handler(bank_handler, Trigger(["банк", "bank"]))
    dp.register_message_handler(credit_handler, Trigger(["кредит", "credit", "займ"]))

    # Deposit commands
    dp.register_message_handler(
        deposit_handler, Trigger(["деп", "депозит", "dep", "deposit"])
    )

    # Pet commands
    dp.register_message_handler(
        pets_handler, Trigger(["pet", "pets", "питомец", "питомцы", "пет", "пэт"])
    )

    # Item commands
    dp.register_message_handler(
        item_handler,
        Trigger(
            [
                "предмет",
                "предметы",
                "item",
                "items",
                "инв",
                "инвентарь",
                "inv",
                "inventory",
                "продать",
            ]
        ),
    )

    # Pay commands
    dp.register_message_handler(pay_handler, Trigger(["pay", "передать", "дать"]))

    # Games
    #    Кубик
    dp.register_message_handler(dice_handler, Trigger(["кубик", "dice"]))

    #    Казино
    dp.register_message_handler(casino_handler, Trigger(["казино", "казик", "casino"]))

    #    Рулетка
    dp.register_message_handler(roulette_handler, Trigger(["Рулетка", "roulette"]))

    #    Nvuti
    dp.register_message_handler(nvuti_handler, Trigger(["нвути", "бм", "nvuti"]))

    #    Кейсы
    dp.register_message_handler(
        cases_handler, Trigger(["кейс", "кейсы", "case", "cases"])
    )

    # Promo-code command
    dp.register_message_handler(
        activatepromo_handler, Trigger(["promo", "promocode", "промокод", "промо"])
    )

    # Bonus command
    dp.register_message_handler(
        bonus_handler, Trigger(["bonus", "бонус", "gift", "подарок"])
    )

    # Referral system
    dp.register_message_handler(refferal_handler, Trigger(["Рефералка", "Ref", "Реф"]))

    # Houses system
    dp.register_message_handler(house_handler, Trigger(["дом", "house", "дома"]))

    # Business system
    dp.register_message_handler(
        business_handler,
        Trigger(["бизнес", "бизнесса", "бизнеса", "бизнесс", "business", "биз"]),
    )

    # Cars system
    dp.register_message_handler(
        cars_handler, Trigger(["car", "cars", "машина", "машины", "карс", "кар"])
    )

    # Yaxti system
    dp.register_message_handler(yaxti_handler, Trigger(["яхта", "яхты"]))

    # Airplanes system
    dp.register_message_handler(
        airplanes_handler, Trigger(["airplane", "airplanes", "самолёт", "самолёты"])
    )

    # Tanki system
    dp.register_message_handler(
        tanki_handler, Trigger(["танки", "танк", "tank", "tanki"])
    )

    # Vertoleti system
    dp.register_message_handler(
        vertoleti_handler,
        Trigger(
            ["вертолёт", "вертушка", "вертушки", "вертолёты", "вертолет", "вертолёты"]
        ),
    )

    # Moto system
    dp.register_message_handler(
        moto_handler, Trigger(["moto", "мото", "мотоцикл", "motorcycle", "мотоциклы"])
    )

    # Mine system
    dp.register_message_handler(mine_handler, Trigger(["шахта", "копать"]))

    # Zavod system
    dp.register_message_handler(zavod_handler, Trigger(["завод", "работать"]))

    # Job system
    dp.register_message_handler(
        jobs_handler,
        Trigger(
            [
                "job",
                "работа",
                "jobs",
                "работы",
                "професия",
                "проффесия",
                "профессии",
                "професии",
                "проффессии",
                "профессия",
            ]
        ),
    )

    # Family system
    dp.register_message_handler(
        marry_handler, Trigger(["marry", "семья", "брак", "браки", "marries"])
    )
    dp.register_callback_query_handler(marry_call_handler, text_startswith="m")

    # Nalogs
    dp.register_message_handler(nalogs_handler, Trigger(["налог", "налоги"]))
    dp.register_message_handler(
        autonalog_handler,
        Trigger(
            ["автоналоги", "авто-налоги", "autonalogi", "autonalogs", "autoналоги"]
        ),
    )

    # Last
    dp.register_message_handler(
        nedavno_handler, Trigger(["недавние", "последнее", "логи", "ласт", "last"])
    )

    # Donate
    dp.register_message_handler(
        donate_handler,
        Trigger(
            [
                "donate",
                "донат",
                "купить",
                "прива",
                "привы",
                "привилегии",
                "привилегия",
                "донаты",
                "donates",
                "donats",
            ]
        ),
    )
    dp.register_message_handler(zadonatit_handler, Trigger(["задонатить", "donatit"]))
    dp.register_message_handler(cobmen_handler, Trigger(["кобмен", "кобменять"]))
    dp.register_message_handler(obmen_handler, Trigger(["обмен", "обменять"]))
    dp.register_message_handler(percent_buy_handler, Trigger(["процент", "percent"]))

    dp.register_callback_query_handler(zadonatit_handler, text="donate")

    dp.register_callback_query_handler(other_method_handler, text="donate_other")
    dp.register_callback_query_handler(payok_handler, text="donate_payok")
    dp.register_message_handler(payok_step1, state=Payok.start)
    dp.register_callback_query_handler(payok_check, state="*", text_startswith="check_")
    dp.register_callback_query_handler(freekassa_handler, text="donate_fk")
    dp.register_message_handler(freekassa_step1, state=Freekassa.start)

    #    # Moderation

    #    dp.register_message_handler(mute_handler, Trigger(['mute', 'мут', 'мьют']))

    #    dp.register_message_handler(ban_handler, Trigger(['ban', 'бан']))

    #    dp.register_message_handler(unmute_handler, Trigger(['unmute', 'анмут', 'размут']))

    #    dp.register_message_handler(unban_handler, Trigger(['unban', 'разбан', 'анбан']))

    #

    #    dp.register_callback_query_handler(unmute_handler, text_startswith='unmute', state='*', chat_type=['group',

    #

    # Oreshka
    dp.register_message_handler(oreshka_handler, Trigger(["орешка", "флип", "flip"]))

    # Prefixes
    dp.register_message_handler(
        prefix_handler,
        Trigger(
            [
                "преф",
                "префы",
                "префиксы",
                "префикс",
                "pref",
                "prefs",
                "prefix",
                "prefixes",
            ]
        ),
    )

    # Rockets
    dp.register_message_handler(
        rocket_handler, Trigger(["ракета", "ракеты", "rocket", "rockets"])
    )

    # Bitcoin
    dp.register_message_handler(
        bitcoin_handler, Trigger(["btc", "биткоин", "бтс", "бтц", "биткоины"])
    )
    dp.register_message_handler(
        videocards_handler,
        Trigger(["видео", "видеокарт", "видеокарта", "видеокарты", "видюха", "видюхи"]),
    )
    dp.register_message_handler(
        ferma_handler, Trigger(["ферма", "майнинг", "ferma", "ferm", "фермы"])
    )
    dp.register_message_handler(bitcoin_handler, Trigger(["курс"]))

    # Rob
    dp.register_message_handler(
        rob_handler,
        Trigger(["rob", "огра", "ограбление", "украсть", "ограбить", "ограба"]),
    )
    dp.register_message_handler(shield_handler, Trigger(["щит", "щиты", "shield"]))

    # Bottles
    dp.register_message_handler(
        bottles_handler, Trigger(["бутылка", "бутылки", "bottles", "бутылк"])
    )

    # Bowling
    dp.register_message_handler(
        bowling_handler, Trigger(["боулинг", "bow", "боу", "боулин", "bowling"])
    )

    # Darts
    dp.register_message_handler(
        darts_handler, Trigger(["дартс", "dart", "дарт", "darts"])
    )

    # KNB
    dp.register_message_handler(
        cnb_handler, Trigger(["cnb", "кнб", "камень-ножницы-бумага", "цу-е-фа"])
    )

    # Euro
    dp.register_message_handler(euro_handler, Trigger(["euro", "евро", "эвро", "еуро"]))
    dp.register_message_handler(
        uah_handler, Trigger(["грн", "гривны", "гривна", "uah"])
    )

    # Страны
    dp.register_message_handler(
        countries_handler,
        Trigger(["страны", "contries", "государства", "страна", "государство"]),
    )
    dp.register_message_handler(country_create_handler, Trigger("создать страну"))

    # My
    dp.register_message_handler(my_country_handler, Trigger("моя страна"))
    dp.register_message_handler(join_country_handler, Trigger("зайти в страну"))
    dp.register_message_handler(leave_country_handler, Trigger("выйти из страны"))

    # Army
    dp.register_message_handler(army_tech_handler, Trigger("Армия техника"))
    dp.register_message_handler(army_snaraj_handler, Trigger("Армия снаряжение"))
    dp.register_message_handler(army_rockets_handler, Trigger("Армия ракеты"))
    dp.register_message_handler(army_gotov_handler, Trigger("Армия готовность"))
    dp.register_message_handler(army_handler, Trigger("армия"))

    # Овнерс
    dp.register_message_handler(get_country_handler, Trigger("Стать президентом"))
    dp.register_message_handler(leave_from_country_handler, Trigger("Уйти из страны"))
    dp.register_message_handler(snyat_budget_country, Trigger("Снять бюджет"))
    dp.register_message_handler(give_budget_country, Trigger("Пополнить бюджет"))

    # Soyuz
    dp.register_message_handler(soyuz_handler, Trigger("Создать союз"))
    dp.register_message_handler(cancel_soyuz_handler, Trigger("Разорвать союз"))

    # War
    dp.register_message_handler(wars_handler, Trigger("Обьявить войну"))
    dp.register_message_handler(wars_handler, Trigger("Объявить войну"))
    # dp.register_message_handler(cancel_wars_handler, Trigger('Отменить войну'))

    # Боссы
    dp.register_message_handler(
        bosses_handler, Trigger(["босс", "боссы", "босы", "бос"])
    )

    # Shop
    dp.register_message_handler(users_shop_handler, Trigger(["shop", "шоп", "магазин"]))

    # Skins
    dp.register_message_handler(
        skins_handler, Trigger(["скины", "скин", "skin", "skins"])
    )
    dp.register_callback_query_handler(skin_call, text_startswith="skin_", state="*")

    # RP
    dp.register_message_handler(
        rp_commands_handler, Trigger(["рп"] + list(emojis.keys()))
    )

    # Other
    dp.register_message_handler(time_handler, Trigger(["time", "время"]))
