from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.types import ReplyKeyboardMarkup, ReplyKeyboardRemove

from config import bot_name

invite_kb = InlineKeyboardMarkup(row_width=2)
invite_kb.insert(InlineKeyboardButton(text='🪄 Добавить в чат', url=f'https://t.me/{bot_name}?startgroup=1'))
invite_kb.insert(InlineKeyboardButton(text='🧑‍🎄 Промокоды', url='https://t.me/barleygame'))
invite_kb.insert(InlineKeyboardButton(text='📃 Документация', url='https://teletype.in/@lordcodes/barley'))

check_ls_kb = InlineKeyboardMarkup(row_width=1)
check_ls_kb.insert(InlineKeyboardButton(text='🔗 Перейти в бота', url=f'https://t.me/{bot_name}'))


def marry_kb(user1, _):
    kb = InlineKeyboardMarkup(row_width=2)
    kb.insert(InlineKeyboardButton(text='✅ Принять', callback_data=f'maccept_{user1}'))
    kb.insert(InlineKeyboardButton(text='❌ Отклонить', callback_data=f'mdecline_{user1}'))
    return kb


admin_kb = InlineKeyboardMarkup(row_width=2)
admin_kb.insert(InlineKeyboardButton(text='👤 Рассылка', callback_data='rass_users'))
admin_kb.insert(InlineKeyboardButton(text='💭 Рассылка', callback_data='rass_chats'))
admin_kb.insert(InlineKeyboardButton(text='Запланировать бд 🔗', callback_data='plan'))
admin_kb.insert(InlineKeyboardButton(text='📃 Список чатов', callback_data='allchats'))


cancel = ReplyKeyboardMarkup(resize_keyboard=True).add('❌')
remove = ReplyKeyboardRemove()


donate_kb = InlineKeyboardMarkup(row_width=1)
donate_kb.add(InlineKeyboardButton(text='🎄 Получить коины', switch_inline_query_current_chat="задонатить"))

donate_kbi = InlineKeyboardMarkup(row_width=1)
donate_kbi.add(InlineKeyboardButton(text='🎄 Получить коины', callback_data='donate'))

back_donate = InlineKeyboardMarkup(row_width=1)
back_donate.insert(InlineKeyboardButton(text='🅰️ Написать админу', url='https://t.me/lord_code'))
back_donate.insert(InlineKeyboardButton(text='🎄 Вернуться назад', callback_data='donate'))


link_to_owner = InlineKeyboardMarkup(row_width=1)
link_to_owner.add(InlineKeyboardButton(text='🅰️ Написать админу', url='https://t.me/lord_code'))


def unmute_kb(user_id: int):
    kb = InlineKeyboardMarkup(row_width=1)
    kb.add(InlineKeyboardButton(text='🔗 Размутить', callback_data=f'unmute_{user_id}'))
    return kb


def unban_kb(user_id: int):
    kb = InlineKeyboardMarkup(row_width=1)
    kb.add(InlineKeyboardButton(text='🔗 Разбанить', callback_data=f'unban_{user_id}'))
    return kb


def oplata_kb(payment: int, url: str):
    kb = InlineKeyboardMarkup(row_width=2)
    kb.insert(InlineKeyboardButton(text='💰 Оплатить', url=url))
    kb.insert(InlineKeyboardButton(text='🅰️ Помощь', url='https://t.me/lord_code'))
    kb.add(InlineKeyboardButton(text='✅ Я оплатил', callback_data=f'check_{payment}'))
    return kb


def oplata_url_kb(url: str):
    kb = InlineKeyboardMarkup(row_width=2)
    kb.insert(InlineKeyboardButton(text='💰 Оплатить', url=url))
    kb.insert(InlineKeyboardButton(text='🅰️ Помощь', url='https://t.me/lord_code'))
    return kb


donates_kb = InlineKeyboardMarkup(row_width=2)
donates_kb.insert(InlineKeyboardButton(text='💰 Payok.io', callback_data='donate_payok'))
donates_kb.insert(InlineKeyboardButton(text='💰 Freekassa', callback_data='donate_fk'))
donates_kb.insert(InlineKeyboardButton(text='💰 Прочее', callback_data='donate_other'))

inv_kb = InlineKeyboardMarkup(row_width=2)
inv_kb.insert(InlineKeyboardButton(text='💲 Продать всё', switch_inline_query_current_chat='Инв продать всё'))

nalogs_all_kb = InlineKeyboardMarkup(row_width=1)
nalogs_all_kb.add(InlineKeyboardButton(text='💲 Оплатить всё', switch_inline_query_current_chat='Налоги оплатить'))

prefix_buy_kb = InlineKeyboardMarkup(row_width=1)
prefix_buy_kb.add(InlineKeyboardButton(text='⭐ Купить префикс', switch_inline_query_current_chat='Префикс купить '))

top_kb = InlineKeyboardMarkup(row_width=3)
top_kb.insert(InlineKeyboardButton(text='💲 Деньги', switch_inline_query_current_chat='Топ руки'))
top_kb.insert(InlineKeyboardButton(text='💳 Деп', switch_inline_query_current_chat='Топ деп'))
top_kb.insert(InlineKeyboardButton(text='💶 Банк', switch_inline_query_current_chat='Топ банк'))
top_kb.insert(InlineKeyboardButton(text='🎡 Общий', switch_inline_query_current_chat='Топ общий'))
top_kb.insert(InlineKeyboardButton(text='⭐ LVL', switch_inline_query_current_chat='Топ уровень'))
top_kb.insert(InlineKeyboardButton(text='👪 Фамы', switch_inline_query_current_chat='Топ браки'))
top_kb.insert(InlineKeyboardButton(text='🤴🏿 Реф', switch_inline_query_current_chat='Топ рефы'))
