from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

countries_main_kb = InlineKeyboardMarkup(row_width=2)
countries_main_kb.insert(InlineKeyboardButton("🔍 Страна", switch_inline_query_current_chat='Страна '))
countries_main_kb.insert(InlineKeyboardButton("📃 Список", switch_inline_query_current_chat='Страны список'))
countries_main_kb.add(InlineKeyboardButton(text='🏳️‍⚧️ Моя страна', switch_inline_query_current_chat='Моя страна'))

country_kb = InlineKeyboardMarkup(row_width=2)
country_kb.insert(InlineKeyboardButton(text='🪖 Воевать', switch_inline_query_current_chat='Обьявить войну '))
country_kb.insert(InlineKeyboardButton(text='😇 Создать союз', switch_inline_query_current_chat='Создать союз'))
country_kb.insert(InlineKeyboardButton(text='🪖 Армия', switch_inline_query_current_chat='Армия'))
country_kb.insert(InlineKeyboardButton(text='🛅 Уйти из страны', switch_inline_query_current_chat='Уйти из страны'))


def join_to_country_kb(country_name: str = ''):
    kb = InlineKeyboardMarkup(row_width=1)
    kb.add(InlineKeyboardButton(text='👆🏼 Получить гражданство', switch_inline_query_current_chat=f'Зайти в страну '
                                                                                                 f'{country_name}'))
    return kb


def get_country_kb(country_name: str = ''):
    kb = InlineKeyboardMarkup(row_width=1)
    kb.add(InlineKeyboardButton(text='🦋 Стать президентом', switch_inline_query_current_chat=f'Стать президентом '
                                                                                             f'{country_name}'))
    return kb


army_kb = InlineKeyboardMarkup(row_width=2)
army_kb.insert(InlineKeyboardButton(text='🛒 Техника', switch_inline_query_current_chat='Армия техника '))
army_kb.insert(InlineKeyboardButton(text='Сняражение 🛒', switch_inline_query_current_chat='Армия снаряжение'))
army_kb.insert(InlineKeyboardButton(text='🛒 Ракеты', switch_inline_query_current_chat='Армия ракеты'))
army_kb.insert(InlineKeyboardButton(text='👮🏼 Готовность', switch_inline_query_current_chat='Армия готовность'))
