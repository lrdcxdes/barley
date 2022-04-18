from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


euro_kb = InlineKeyboardMarkup(row_width=2)
euro_kb.insert(InlineKeyboardButton(text='💶 Купить', switch_inline_query_current_chat='Евро купить '))
euro_kb.insert(InlineKeyboardButton(text='🪝 Продать', switch_inline_query_current_chat='Евро продать '))
euro_kb.add(InlineKeyboardButton(text='🥫 Улучшить', switch_inline_query_current_chat='Евро буст '))


my_euro_kb = InlineKeyboardMarkup(row_width=1)
my_euro_kb.add(InlineKeyboardButton(text='💶 Мой сейф', switch_inline_query_current_chat='Евро'))

uah_kb = InlineKeyboardMarkup(row_width=2)
uah_kb.insert(InlineKeyboardButton(text='💶 Купить', switch_inline_query_current_chat='Гривны купить '))
uah_kb.insert(InlineKeyboardButton(text='🪝 Продать', switch_inline_query_current_chat='Гривны продать '))
uah_kb.add(InlineKeyboardButton(text='🥫 Улучшить', switch_inline_query_current_chat='Гривны буст '))


my_uah_kb = InlineKeyboardMarkup(row_width=1)
my_uah_kb.add(InlineKeyboardButton(text='💶 Мой сейф', switch_inline_query_current_chat='Гривны'))
