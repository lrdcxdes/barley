from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


skin_buy_kb = InlineKeyboardMarkup(row_width=2)
skin_buy_kb.insert(InlineKeyboardButton(text="🛒 Купить", switch_inline_query_current_chat='Скин купить '))
skin_buy_kb.insert(InlineKeyboardButton(text="👔 Мой скин", switch_inline_query_current_chat='Скин'))


def skin_kb(user_id: int, skin_id: int):
    kb = InlineKeyboardMarkup(row_width=2)
    kb.insert(InlineKeyboardButton(text='😃 Лицо', callback_data=f'skin_{skin_id}_{user_id}_front'))
    kb.insert(InlineKeyboardButton(text='🔙 Спина', callback_data=f'skin_{skin_id}_{user_id}_back'))
    kb.add(InlineKeyboardButton(text='🍑 Снизу', callback_data=f'skin_{skin_id}_{user_id}_down'))
    return kb
