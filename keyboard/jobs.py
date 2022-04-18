from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


jobs_kb = InlineKeyboardMarkup(row_width=1)
jobs_kb.add(InlineKeyboardButton(text='💸 Дать взятку', switch_inline_query_current_chat='Работа взятка'))
jobs_kb.add(InlineKeyboardButton(text='💪🏿 Устроиться', switch_inline_query_current_chat='Работа устроиться '))

rabotat_kb = InlineKeyboardMarkup(row_width=1)
rabotat_kb.add(InlineKeyboardButton(text='💪🏿 Работать', switch_inline_query_current_chat='Завод работать'))

shaxta_kb = InlineKeyboardMarkup(row_width=1)
shaxta_kb.add(InlineKeyboardButton(text='💪🏿 Копать', switch_inline_query_current_chat='Шахта копать'))

bottle_kb = InlineKeyboardMarkup(row_width=1)
bottle_kb.add(InlineKeyboardButton(text='💪🏿 Собирать', switch_inline_query_current_chat='Бутылки собирать'))

report_kb = InlineKeyboardMarkup(row_width=1)
report_kb.add(InlineKeyboardButton(text='🆘 Рассказать о баге', url='https://t.me/lord_code'))
