from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


marrye_kb = InlineKeyboardMarkup(row_width=2)
marrye_kb.insert(InlineKeyboardButton(text='💲 Снять', switch_inline_query_current_chat='Семья снять '))
marrye_kb.insert(InlineKeyboardButton(text='💸 Положить', switch_inline_query_current_chat='Семья положить '))
marrye_kb.insert(InlineKeyboardButton(text='🆙 Бустануть', switch_inline_query_current_chat='Семья буст'))
marrye_kb.insert(InlineKeyboardButton(text='❌ Удалить', switch_inline_query_current_chat='Семья снять '))
